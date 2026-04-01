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
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UNIVERSAL AI INITIALIZATION ---
@st.cache_resource
def get_ai_model():
    try:
        if "GEMINI_KEY" not in st.secrets:
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Probe for working model
        for name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
            try:
                m = genai.GenerativeModel(name)
                m.generate_content("Hi")
                return m
            except: continue
        return None
    except: return None

if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = get_ai_model()

# --- 4. IMPROVED SEARCH ENGINE ---
def find_topic_in_pdf(pdf_path, query):
    try:
        doc = fitz.open(pdf_path)
        
        # STOP-WORD FILTER: Ignore common filler words
        stop_words = {"can", "you", "show", "me", "the", "of", "a", "an", "is", "diagram", "draw", "explain", "please", "find"}
        keywords = [word for word in query.lower().split() if word not in stop_words and len(word) > 2]
        
        if not keywords: # Fallback if user only typed stop words
            keywords = query.lower().split()

        best_page = None
        max_hits = 0
        
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            # Count how many unique keywords appear on this page
            hits = sum(1 for kw in keywords if kw in text)
            if hits > max_hits:
                max_hits = hits
                best_page = page_num

        # We only return a result if we found at least one strong keyword match
        if best_page is not None and max_hits > 0:
            start = max(0, best_page - 1)
            end = min(len(doc), best_page + 2)
            context_text = ""
            for i in range(start, end):
                context_text += doc[i].get_text() + "\n"
            
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
if not os.path.exists(SYLLABUS_DIR):
    os.makedirs(SYLLABUS_DIR)

# Sidebar Info
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])
st.sidebar.title("📚 Library Status")
if pdf_files:
    st.sidebar.success(f"Books Loaded: {len(pdf_files)}")
    with st.sidebar.expander("See Available Chapters"):
        for f in pdf_files: st.write(f"• {f}")
else:
    st.sidebar.error("No PDFs found in 'ncert_syllabus' on GitHub.")

mode = st.sidebar.radio("Search Mode:", ["Global (All Books)", "Single Chapter"])
selected_chap = None
if mode == "Single Chapter" and pdf_files:
    selected_chap = st.sidebar.selectbox("📂 Choose Chapter", pdf_files)

# Chat History
if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m and m["image"]: st.image(m["image"])

# --- SEARCH LOGIC ---
if prompt := st.chat_input("Search (e.g. Human Eye, Ohm's Law, Respiration)"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        found_txt, found_img, p_no, source_file = "", None, 0, ""
        
        with st.spinner("🔍 Scanning NCERT Library..."):
            targets = [selected_chap] if mode == "Single Chapter" and selected_chap else pdf_files
            
            for file in targets:
                path = os.path.join(SYLLABUS_DIR, file)
                txt, img, page = find_topic_in_pdf(path, prompt)
                if txt:
                    found_txt, found_img, p_no, source_file = txt, img, page, file
                    break 

        if found_txt:
            if st.session_state.ai_brain:
                try:
                    # Send only relevant context to AI
                    ai_prompt = f"Using NCERT text: {found_txt[:4000]}. Answer: {prompt}."
                    response = st.session_state.ai_brain.generate_content(ai_prompt)
                    ans = f"{response.text}\n\n**📍 Source: {source_file} (Page {p_no})**"
                    
                    st.markdown(ans)
                    if found_img: st.image(found_img, caption=f"NCERT Diagram: {prompt}")
                    st.session_state.history.append({"role": "assistant", "content": ans, "image": found_img})
                except Exception as e:
                    st.error(f"Topic found in {source_file}, but AI is busy. Here is the page image:")
                    if found_img: st.image(found_img)
            else:
                st.warning(f"Topic found in {source_file} (Page {p_no}), but AI is not configured. Check your API Key.")
                if found_img: st.image(found_img)
        else:
            st.error("❌ Topic not found. Try simpler keywords like 'Eye', 'Heart', or 'Acid'.")

st.sidebar.markdown("---")
st.sidebar.caption("Syllabus: CBSE 2026-27")
