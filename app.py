import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
import re
import os
import io

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Global Hub", page_icon="🧪", layout="wide")

# --- 2. STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #1E88E5; font-weight: bold; text-align: center; }
    .source-tag { color: #546E7A; font-size: 14px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UNIVERSAL AI INITIALIZATION (FIXES 404) ---
def get_ai_model():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Missing GEMINI_KEY in Secrets!")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # We try to 'probe' for a working model name
        # Some accounts use 'gemini-1.5-flash', some use 'models/gemini-1.5-flash'
        test_names = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro", "models/gemini-pro"]
        
        for name in test_names:
            try:
                model = genai.GenerativeModel(name)
                # Quick test call
                model.generate_content("Hi")
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        return None

if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = get_ai_model()

# --- 4. SMART PDF SEARCH ---
def find_topic_in_pdf(pdf_path, query):
    try:
        doc = fitz.open(pdf_path)
        keywords = query.lower().split()
        
        best_page = None
        max_hits = 0
        
        # Scanning for the best match
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            hits = sum(1 for kw in keywords if kw in text)
            if hits > max_hits:
                max_hits = hits
                best_page = page_num

        if best_page is not None:
            # Extract text from 3 pages (previous, current, next)
            start = max(0, best_page - 1)
            end = min(len(doc), best_page + 2)
            context_text = ""
            for i in range(start, end):
                context_text += doc[i].get_text() + "\n"
            
            # Create high-res screenshot
            page = doc.load_page(best_page)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            img = Image.open(io.BytesIO(pix.tobytes()))
            
            return context_text, img, best_page + 1
        return None, None, None
    except:
        return None, None, None

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Global Science Hub</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Navigation
st.sidebar.title("🚀 Study Navigation")
mode = st.sidebar.radio("Search Mode:", ["Global (All Chapters)", "Single Chapter"])

selected_chap = None
if mode == "Single Chapter" and pdf_files:
    selected_chap = st.sidebar.selectbox("📂 Choose Chapter", pdf_files)

# Chat State
if "history" not in st.session_state: st.session_state.history = []

# Display Messages
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m and m["image"]:
            st.image(m["image"], caption="Textbook Context")

# Input
if prompt := st.chat_input("Ask a question (e.g., Draw human eye, Explain Ohm's Law)..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        found_txt, found_img, p_no, source_file = "", None, 0, ""
        
        with st.spinner("Searching NCERT Books..."):
            targets = [selected_chap] if mode == "Single Chapter" else pdf_files
            for file in targets:
                path = os.path.join(SYLLABUS_DIR, file)
                txt, img, page = find_topic_in_pdf(path, prompt)
                if txt:
                    found_txt, found_img, p_no, source_file = txt, img, page, file
                    break # Stop at first best match

        if st.session_state.ai_brain and found_txt:
            try:
                # Optimized for Free Tier (Reduced context to 4000 chars)
                ai_prompt = f"""
                You are a CBSE Science Teacher. Use this text: {found_txt[:4000]}
                Answer this: {prompt}
                Rules: Use simple Class 10 terms. Mention Board Tips.
                """
                response = st.session_state.ai_brain.generate_content(ai_prompt)
                ans = f"{response.text}\n\n**📍 Source: {source_file} (Page {p_no})**"
                
                st.markdown(ans)
                if found_img: st.image(found_img, caption=f"Diagram from {source_file}")
                
                st.session_state.history.append({"role": "assistant", "content": ans, "image": found_img})
            except Exception as e:
                st.error(f"AI could not process the answer: {e}")
        else:
            st.warning("Could not find this topic in the books. Please try different keywords!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE 2026-27 | Digital Tutor")
