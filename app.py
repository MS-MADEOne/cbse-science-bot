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

# --- 3. AUTO-DISCOVERY AI ENGINE ---
@st.cache_resource
def init_ai():
    try:
        if "GEMINI_KEY" not in st.secrets: return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Find best available model
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else "models/gemini-pro"
        return genai.GenerativeModel(name)
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

ai_model = init_ai()

# --- 4. SMART PDF SEARCH & SCREENSHOT ---
def find_topic_in_pdf(pdf_path, query):
    """Searches PDF and returns relevant text and page image"""
    doc = fitz.open(pdf_path)
    keywords = query.lower().split()
    
    best_page = None
    extracted_text = ""
    
    # Search for the best page (where most keywords appear)
    max_hits = 0
    for page_num, page in enumerate(doc):
        text = page.get_text()
        hits = sum(1 for kw in keywords if kw in text.lower())
        if hits > max_hits:
            max_hits = hits
            best_page = page_num
            # Get text from current, previous and next page for context
            start = max(0, page_num - 1)
            end = min(len(doc), page_num + 2)
            extracted_text = ""
            for i in range(start, end):
                extracted_text += doc[i].get_text() + "\n"

    if best_page is not None:
        # Generate Screenshot of the best page
        page = doc.load_page(best_page)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)) # Standard Res
        img = Image.open(io.BytesIO(pix.tobytes()))
        return extracted_text, img, best_page + 1
    
    return None, None, None

# --- 5. MAIN APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Global Science Hub</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Mode Selection
st.sidebar.title("🚀 Navigation")
mode = st.sidebar.radio("Study Mode:", ["Global Search (All Books)", "Chapter Wise"])

selected_chapter = None
if mode == "Chapter Wise" and pdf_files:
    selected_chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Messages
for m in st.session_state.chat_history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m and m["image"]:
            st.image(m["image"], caption="Relevant Textbook Page")

# User Interaction
if prompt := st.chat_input("Search any topic (e.g., Human Eye Diagram, Ohm's Law)..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        final_text = ""
        final_img = None
        source_info = ""

        # SCANNING FILES
        with st.spinner("🔍 Searching through NCERT Library..."):
            files_to_scan = [selected_chapter] if mode == "Chapter Wise" else pdf_files
            
            for file_name in files_to_scan:
                path = os.path.join(SYLLABUS_DIR, file_name)
                text, img, p_no = find_topic_in_pdf(path, prompt)
                if text:
                    final_text = text
                    final_img = img
                    source_info = f"Source: {file_name} | Page: {p_no}"
                    break # Found the best match, stop searching

        # AI EXPLANATION
        if ai_model and final_text:
            try:
                # Optimized AI prompt with smaller context (5000 chars)
                ai_prompt = f"""
                You are a CBSE Science Teacher. Use this NCERT text: {final_text[:5000]}
                Answer this student question: {prompt}
                
                Guidelines:
                1. Provide a clear Class 10 level explanation.
                2. Mention any formulas or laws found in the text.
                3. Keep the answer exam-focused.
                """
                response = ai_model.generate_content(ai_prompt)
                full_response = f"{response.text}\n\n**📍 {source_info}**"
                
                st.markdown(full_response)
                if final_img:
                    st.image(final_img, caption="Diagram from Textbook")
                
                # Save to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response,
                    "image": final_img
                })
            except Exception as e:
                st.error(f"AI Error: {e}")
                st.info("The topic was found in the book, but the AI is currently hitting a rate limit. Please try again in 30 seconds.")
        else:
            st.warning("⚠️ Topic not found in the uploaded PDFs. Try checking your spelling or keywords!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE 2026-27 | Digital Guru")
