import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🧪", layout="wide")

# --- 2. STYLING (Bento & Flashcards) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; }
    .info-card { padding: 18px; border-radius: 15px; color: white; margin-bottom: 10px; min-height: 150px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    .flashcard { background: #fdfdfd; border-radius: 12px; padding: 12px; border-left: 6px solid #3B82F6; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 3px 10px; border-radius: 50px; font-weight: 700; margin: 3px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINES ---
@st.cache_resource
def init_ai():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0]
        return genai.GenerativeModel(name)
    except: return None

ai_model = init_ai()

@st.cache_data
def get_pdf_text(path):
    with open(path, "rb") as f:
        pdf = pypdf.PdfReader(f)
        return re.sub(r'[^\x00-\x7F]+', ' ', "".join([p.extract_text() for p in pdf.pages])).strip()

def get_image(q):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={q}"
        return requests.get(url).json()['query']['pages'][0]['original']['source']
    except: return None

# --- 4. ONE-CALL GENERATOR (SAVES TIME) ---
def generate_study_kit(chapter_name, text):
    """Generates everything in ONE API call instead of three"""
    prompt = f"""
    Analyze the chapter '{chapter_name}' from this text: {text[:5000]}
    
    Provide the following sections strictly using these tags:
    SECTION_BENTO:
    - Concept: [1 sentence]
    - Application: [1 sentence]
    - Experiment: [1 sentence]
    - ExamFocus: [1 sentence]
    
    SECTION_FORMULAS:
    [List 4-5 major formulas or chemical equations]
    
    SECTION_TIPS:
    [List 4 board exam tips]
    """
    try:
        res = ai_model.generate_content(prompt).text
        return res
    except: return "Error generating kit."

# --- 5. MAIN APP ---
st.markdown("<h1 class='main-title'>🚀 CBSE Science Hub Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    
    # Check if chapter changed - Clear cache for new chapter
    if "current_chap" not in st.session_state or st.session_state.current_chap != chapter:
        st.session_state.current_chap = chapter
        st.session_state.raw_text = get_pdf_text(os.path.join(SYLLABUS_DIR, chapter))
        st.session_state.study_kit = None # Reset kit for new chapter

    # Button to generate visual kit (Only if not already generated)
    if not st.session_state.study_kit:
        if st.sidebar.button("✨ Generate Visual Study Kit"):
            with st.spinner("Creating your Infographics..."):
                st.session_state.study_kit = generate_study_kit(chapter, st.session_state.raw_text)
                st.sidebar.success("Study Kit Ready!")
else:
    st.sidebar.warning("Upload PDFs to GitHub!")
    st.stop()

# --- 6. TABS ---
chat_tab, info_tab, cheat_tab = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

with chat_tab:
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Ask about this chapter..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            try:
                res = ai_model.generate_content(f"Context: {st.session_state.raw_text[:6000]}. Answer: {p}").text
                st.markdown(res)
                st.session_state.msgs.append({"role": "assistant", "content": res})
            except: st.error("AI Busy.")

with info_tab:
    if st.session_state.study_kit:
        kit = st.session_state.study_kit
        try:
            bento = kit.split("SECTION_BENTO:")[1].split("SECTION_FORMULAS:")[0].strip().split('\n')
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div class="info-card blue-card"><b>🎯 Concept</b><br>{bento[0].replace('- Concept:', '')}</div>
                    <div class="info-card green-card"><b>🌍 Application</b><br>{bento[1].replace('- Application:', '')}</div>
                    <div class="info-card orange-card"><b>🧪 Experiment</b><br>{bento[2].replace('- Experiment:', '')}</div>
                    <div class="info-card purple-card"><b>📈 Weightage</b><br>{bento[3].replace('- ExamFocus:', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                term = chapter.replace(".pdf", "").split("_")[-1]
                img = get_image(term)
                if img: st.image(img, use_container_width=True)
                else: st.info("Diagram in textbook.")
        except: st.warning("Please click 'Generate Visual Study Kit' in the sidebar.")
    else: st.info("Click the button in the sidebar to generate visuals!")

with cheat_tab:
    if st.session_state.study_kit:
        kit = st.session_state.study_kit
        try:
            formulas = kit.split("SECTION_FORMULAS:")[1].split("SECTION_TIPS:")[0].strip().split('\n')
            tips = kit.split("SECTION_TIPS:")[1].strip().split('\n')
            
            cx, cy = st.columns(2)
            with cx:
                st.subheader("🔢 Formula Bank")
                for f in formulas: st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
            with cy:
                st.subheader("🚩 Board Tips")
                for t in tips: st.markdown(f"<div class='flashcard' style='border-left-color:red;'>{t}</div>", unsafe_allow_html=True)
        except: st.error("Kit format error.")
    else: st.info("Click the button in the sidebar to generate Flashcards!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE Science Pro | Optimized")
