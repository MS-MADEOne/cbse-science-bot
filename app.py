import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science Hub 2026-27", page_icon="🧪", layout="wide")

# --- ADVANCED CSS FOR "INFOGRAPHICS" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main-title { font-size:45px; color: #1E3A8A; font-weight: 800; text-align: center; margin-bottom: 30px; }
    
    /* Bento Grid Styling for Infographics */
    .bento-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
    .bento-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #3B82F6; }
    .card-title { font-size: 18px; font-weight: 700; color: #1E40AF; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    .formula-pill { background: #EFF6FF; color: #1E40AF; padding: 5px 12px; border-radius: 20px; font-weight: 600; font-size: 14px; border: 1px solid #BFDBFE; display: inline-block; margin: 5px; }
    
    /* Chat Styling */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .video-btn { background-color: #EF4444; color: white !important; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_wikimedia_image(query):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={query}"
        res = requests.get(url).json()
        return res['query']['pages'][0]['original']['source']
    except: return None

@st.cache_resource
def initialize_bot():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0]
        return genai.GenerativeModel(name)
    except: return None

model = initialize_bot()

@st.cache_data
def load_pdf(path):
    pdf = pypdf.PdfReader(open(path, "rb"))
    text = "".join([p.extract_text() for p in pdf.pages])
    return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()

# --- APP INTERFACE ---
st.markdown("<h1 class='main-title'>🚀 CBSE Class 10 Science Hub</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

if pdf_files:
    selected_file = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    syllabus_text = load_pdf(os.path.join(SYLLABUS_DIR, selected_file))
else:
    st.sidebar.warning("Upload PDFs to GitHub folder!")
    syllabus_text = ""

# --- TABS SYSTEM ---
tab1, tab2, tab3 = st.tabs(["💬 AI Tutor", "📊 Visual Infographics", "📝 Exam Cheat Sheet"])

# --- TAB 1: AI TUTOR ---
with tab1:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            context = syllabus_text[:8000]
            ai_prompt = f"Teacher, answer using this context: {context}. Question: {prompt}. If a process exists, use Graphviz. End with VIDEO_KEYWORD: [topic]"
            res = model.generate_content(ai_prompt).text
            
            # Simple UI cleanup for chat
            if "DIAGRAM_START" in res:
                st.markdown(res.split("DIAGRAM_START")[0])
                st.graphviz_chart(res.split("DIAGRAM_START")[1].split("DIAGRAM_END")[0])
                st.markdown(res.split("DIAGRAM_END")[1])
            else: st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- TAB 2: VISUAL INFOGRAPHICS ---
with tab2:
    if syllabus_text:
        st.subheader("💡 Visual Breakdown")
        with st.spinner("Generating Visual Map..."):
            # Request specific JSON-like data for Infographics
            info_prompt = f"Summarize {selected_file} into 3 categories: 1. Main Concept, 2. Key Process, 3. Image Search Word. Context: {syllabus_text[:4000]}"
            info_res = model.generate_content(info_prompt).text
            
            # Render Bento Grid
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div class="bento-container">
                    <div class="bento-card">
                        <div class="card-title">📖 Chapter Overview</div>
                        <p>{info_res[:500]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Dynamic Image Logic
                img_word = selected_file.replace(".pdf", "").replace("_", " ")
                img_url = get_wikimedia_image(img_word)
                if img_url:
                    st.markdown("<div class='bento-card'><b>🖼️ Reference Diagram</b></div>", unsafe_allow_html=True)
                    st.image(img_url, use_container_width=True)

# --- TAB 3: EXAM CHEAT SHEET ---
with tab3:
    if syllabus_text:
        st.subheader(f"⚡ {selected_file} Cheat Sheet")
        cheat_prompt = f"Extract all formulas and 5 important board exam points from: {syllabus_text[:6000]}"
        cheat_res = model.generate_content(cheat_prompt).text
        
        # Display as a clean list of formulas
        formulas = re.findall(r'(\w+\s*=\s*[\w\d\s/+\-*]+)', cheat_res)
        if formulas:
            st.markdown("### 🔢 Formula Bank")
            for f in formulas:
                st.markdown(f"<span class='formula-pill'>{f}</span>", unsafe_allow_html=True)
        
        st.markdown("### 📝 Must-Know for Boards")
        st.info(cheat_res)

st.sidebar.markdown("---")
st.sidebar.caption("Designed for CBSE 2026-27")
