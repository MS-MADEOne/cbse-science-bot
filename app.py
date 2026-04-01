import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
import re
import os
import io

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Hub Pro", page_icon="🧪", layout="wide")

# --- 2. STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:38px; color: #1565C0; font-weight: bold; text-align: center; }
    .diag-box { border: 2px solid #3B82F6; border-radius: 10px; padding: 5px; background: white; }
    .search-msg { background-color: #e3f2fd; padding: 10px; border-radius: 10px; border-left: 5px solid #2196f3; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI & PDF ENGINES ---
@st.cache_resource
def init_ai_bot():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0]
        return genai.GenerativeModel(name)
    except: return None

ai_model = init_ai_bot()

def get_text_and_diagram(pdf_path, query_word):
    """Searches for text and returns a screenshot of the relevant page"""
    doc = fitz.open(pdf_path)
    full_text = ""
    target_page_num = 0
    
    # 1. Search for the most relevant page
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        full_text += page_text + " "
        if query_word.lower() in page_text.lower():
            target_page_num = page_num
            # We don't break because we want full text, but we keep this page for diagram

    # 2. Extract the diagram page as an image
    page = doc.load_page(target_page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # High resolution
    img_data = Image.open(io.BytesIO(pix.tobytes()))
    
    return full_text, img_data, target_page_num + 1

# --- 4. MAIN APP ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science: Global Hub</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# NAVIGATION MODE
st.sidebar.title("🚀 Study Mode")
mode = st.sidebar.radio("Choose Mode:", ["Chapter Wise", "Global Search (All Books)"])

selected_chapter = None
if mode == "Chapter Wise" and pdf_files:
    selected_chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
elif mode == "Global Search (All Books)":
    st.sidebar.info("Bot will search across all uploaded NCERT chapters!")

# --- 5. LOGIC FOR GLOBAL SEARCH ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# DISPLAY CHAT
for m in st.session_state.chat_history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m: st.image(m["image"], caption="Diagram from NCERT Textbook")

# USER INPUT
if prompt := st.chat_input("Ask anything (e.g., Explain the structure of Nephron)"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        found_text = ""
        found_img = None
        page_ref = ""
        
        with st.spinner("Searching through textbooks..."):
            # If Global, loop through all files. If Chapter, just one.
            files_to_scan = pdf_files if mode == "Global Search (All Books)" else [selected_chapter]
            
            for file in files_to_scan:
                if not file: continue
                path = os.path.join(SYLLABUS_DIR, file)
                # Quick scan for keywords in prompt
                keywords = prompt.split()[-1] # Simplest keyword
                text, img, p_no = get_text_and_diagram(path, keywords)
                
                if text:
                    found_text = text
                    found_img = img
                    page_ref = f"Source: {file}, Page: {p_no}"
                    break

        if ai_model and found_text:
            try:
                # Ask AI to explain using found text
                ai_prompt = f"Using this NCERT data: {found_text[:6000]}. Explain: {prompt}. Give board tips."
                response = ai_model.generate_content(ai_prompt).text
                
                st.markdown(response)
                st.caption(f"📍 {page_ref}")
                
                # Show Diagram if found
                if found_img:
                    st.markdown("### 🖼️ Diagram from Textbook:")
                    st.image(found_img, use_container_width=True)
                
                # Save to history
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"{response}\n\n📍 {page_ref}",
                    "image": found_img
                })
            except:
                st.error("AI is busy. Please try again.")
        else:
            st.warning("Could not find that topic in the textbook. Please try different keywords!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE 2026-27 | Digital Library")
