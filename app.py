import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🧪", layout="wide")

# --- 2. ADVANCED STYLING (Bento Grids & Flashcards) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }

    .main-title { font-size:48px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    
    /* Bento Grid / Infographic Cards */
    .infographic-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
    .info-card { padding: 20px; border-radius: 20px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 15px; min-height: 180px; }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    
    .card-icon { font-size: 28px; margin-bottom: 8px; }
    .card-title { font-size: 19px; font-weight: 800; margin-bottom: 6px; }
    .card-text { font-size: 14px; opacity: 0.95; line-height: 1.5; }

    /* Flashcards */
    .flashcard { background: #fdfdfd; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #1F2937; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 5px 14px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    .exam-tip-card { border-left-color: #EF4444; background: #FFF5F5; border: 1px solid #FED7D7; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTO-DISCOVERY AI SETUP ---
@st.cache_resource
def init_ai_discovery():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Add GEMINI_KEY to Secrets!")
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        prefs = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        final_model = next((m for m in prefs if m in available_models), available_models[0])
        return genai.GenerativeModel(final_model)
    except Exception as e:
        st.error(f"Discovery Error: {e}")
        return None

ai_model = init_ai_discovery()

@st.cache_data
def process_pdf_safe(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            text = "".join([p.extract_text() for p in pdf.pages])
            return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()
    except: return "PDF Load Error"

def get_wiki_img(q):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={q}"
        return requests.get(url).json()['query']['pages'][0]['original']['source']
    except: return None

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🚀 CBSE Science Hub Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    raw_text = process_pdf_safe(os.path.join(SYLLABUS_DIR, chapter))
else:
    st.sidebar.warning("Upload PDFs to GitHub folder!")
    raw_text = ""

# --- 5. TABS SYSTEM ---
chat_tab, info_tab, cheat_tab = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

# --- TAB 1: CHAT TUTOR ---
with chat_tab:
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask a concept..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            if ai_model and raw_text:
                try:
                    res = ai_model.generate_content(f"Context: {raw_text[:6000]}. Explain {p} like a CBSE teacher.").text
                    st.markdown(res)
                    st.session_state.msgs.append({"role": "assistant", "content": res})
                except: st.error("Tutor is busy. Try again!")

# --- TAB 2: VISUAL DASHBOARD ---
with info_tab:
    if raw_text and ai_model:
        st.markdown("### 📊 Interactive Visual Guide")
        with st.spinner("Generating Bento Infographics..."):
            try:
                gen_p = f"Summarize {chapter} into 4 points: CONCEPT, APPLICATION, EXPERIMENT, TIP. Context: {raw_text[:4000]}"
                res_text = ai_model.generate_content(gen_p).text
                pts = res_text.split('*')
                
                c_1, c_2 = st.columns([2, 1])
                with c_1:
                    st.markdown(f"""
                    <div class="infographic-container">
                        <div class="info-card blue-card">
                            <div class="card-icon">🎯</div><div class="card-title">Concept</div>
                            <div class="card-text">{pts[1] if len(pts)>1 else 'Main Logic Loading...'}</div>
                        </div>
                        <div class="info-card green-card">
                            <div class="card-icon">🌍</div><div class="card-title">Application</div>
                            <div class="card-text">{pts[2] if len(pts)>2 else 'Real World Use Loading...'}</div>
                        </div>
                        <div class="info-card orange-card">
                            <div class="card-icon">🧪</div><div class="card-title">Experiment</div>
                            <div class="card-text">{pts[3] if len(pts)>3 else 'Lab Activity Loading...'}</div>
                        </div>
                        <div class="info-card purple-card">
                            <div class="card-icon">📈</div><div class="card-title">Weightage</div>
                            <div class="card-text">{pts[4] if len(pts)>4 else 'Exam Focus Loading...'}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_2:
                    st.markdown("📸 **Diagram Reference**")
                    term = chapter.replace(".pdf", "").split("_")[-1]
                    img = get_wiki_img(term)
                    if img: st.image(img, use_container_width=True)
                    else: st.graphviz_chart("digraph { A[label='Concept'] -> B[label='NCERT Knowledge'] }")
            except: st.warning("Visual generator is reloading...")

# --- TAB 3: EXAM FLASHCARDS ---
with cheat_tab:
    if raw_text and ai_model:
        col_x, col_y = st.columns(2)
        with st.spinner("Writing Flashcards..."):
            try:
                cheat_p = f"From {raw_text[:6000]}, list 4 FORMULAS and 4 BOARD TIPS. Use tags FORMULA: and TIP:"
                cheat_res = ai_model.generate_content(cheat_p).text
                
                with col_x:
                    st.subheader("🔢 Formula Bank")
                    f_list = re.findall(r'FORMULA:\s*(.*)', cheat_res)
                    for f in f_list:
                        st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
                
                with col_y:
                    st.subheader("🚩 Red Alert Tips")
                    t_list = re.findall(r'TIP:\s*(.*)', cheat_res)
                    for t in t_list:
                        st.markdown(f"<div class='flashcard exam-tip-card'><b>Board Tip:</b> {t}</div>", unsafe_allow_html=True)
            except: st.error("Exam data unavailable.")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE Science Pro v2.6 | 2026-27")
