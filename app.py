import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🧪", layout="wide")

# --- ADVANCED BEAUTIFICATION CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }

    .main-title { font-size:50px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    
    /* Bento Grid / Infographic Cards */
    .infographic-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
    .info-card { padding: 20px; border-radius: 20px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 15px; min-height: 200px; }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    
    .card-icon { font-size: 30px; margin-bottom: 10px; }
    .card-title { font-size: 20px; font-weight: 800; margin-bottom: 8px; }
    .card-text { font-size: 14px; opacity: 0.9; line-height: 1.6; }

    /* Cheat Sheet Flashcards */
    .flashcard { background: white; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; color: #1F2937; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 5px; font-size: 13px; }
    .exam-tip { border-left-color: #EF4444; background: #FEF2F2; }
    
    /* Search Bar Sidebar */
    .stTextInput input { border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- IMAGE ENGINE ---
def get_wiki_image(query):
    try:
        # We search specifically for "Scientific Diagram" to get better results
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={query}"
        data = requests.get(url).json()
        return data['query']['pages'][0]['original']['source']
    except: return None

# --- AI SETUP ---
@st.cache_resource
def init_ai():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

ai_model = init_ai()

@st.cache_data
def process_pdf(path):
    pdf = pypdf.PdfReader(open(path, "rb"))
    text = "".join([p.extract_text() for p in pdf.pages])
    return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()

# --- APP UI ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

# SIDEBAR
SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Choose Chapter", pdf_files)
    raw_text = process_pdf(os.path.join(SYLLABUS_DIR, chapter))
    st.sidebar.success(f"Exam Mode: {chapter}")
else:
    st.sidebar.error("Please upload PDFs to 'ncert_syllabus' on GitHub.")
    raw_text = ""

# --- TABS ---
chat_tab, info_tab, cheat_tab = st.tabs(["💬 AI Tutor", "📊 Visual Dashboard", "⚡ Exam Flashcards"])

# --- 1. CHAT TUTOR ---
with chat_tab:
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask me a concept..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            # Teacher context
            prompt = f"Using context: {raw_text[:6000]}. Explain {p} like a CBSE teacher. Draw flowchart using DIAGRAM_START [DOT code] DIAGRAM_END if needed."
            response = ai_model.generate_content(prompt).text
            if "DIAGRAM_START" in response:
                st.markdown(response.split("DIAGRAM_START")[0])
                st.graphviz_chart(response.split("DIAGRAM_START")[1].split("DIAGRAM_END")[0])
                st.markdown(response.split("DIAGRAM_END")[1])
            else: st.markdown(response)
            st.session_state.msgs.append({"role": "assistant", "content": response})

# --- 2. VISUAL INFOGRAPHIC DASHBOARD ---
with info_tab:
    if raw_text:
        st.markdown("### 🗺️ Chapter Mind-Map")
        with st.spinner("Building Infographics..."):
            # AI request for 4 specific bento categories
            sum_prompt = f"Analyze {chapter}. Give 4 distinct sections: 1. CORE CONCEPT, 2. REAL LIFE APP, 3. KEY EXPERIMENT, 4. BOARD WEIGHTAGE. Context: {raw_text[:5000]}"
            res = ai_model.generate_content(sum_prompt).text
            
            # Extract content (very basic parsing for demo)
            parts = res.split('\n\n')
            
            # BENTO GRID DISPLAY
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown(f"""
                <div class="infographic-container">
                    <div class="info-card blue-card">
                        <div class="card-icon">🎯</div>
                        <div class="card-title">Core Concept</div>
                        <div class="card-text">{parts[0] if len(parts)>0 else 'Loading...'}</div>
                    </div>
                    <div class="info-card green-card">
                        <div class="card-icon">🌍</div>
                        <div class="card-title">Real-Life Application</div>
                        <div class="card-text">{parts[1] if len(parts)>1 else 'Loading...'}</div>
                    </div>
                    <div class="info-card orange-card">
                        <div class="card-icon">🧪</div>
                        <div class="card-title">Key Experiment</div>
                        <div class="card-text">{parts[2] if len(parts)>2 else 'Loading...'}</div>
                    </div>
                    <div class="info-card purple-card">
                        <div class="card-icon">📊</div>
                        <div class="card-title">Board Exam Focus</div>
                        <div class="card-text">{parts[3] if len(parts)>3 else 'Loading...'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown("🔍 **Topic Visualization**")
                # Image search word based on chapter
                search_term = chapter.replace(".pdf", "").split("_")[-1]
                img_url = get_wiki_image(search_term)
                if img_url:
                    st.image(img_url, caption=f"NCERT Diagram: {search_term}", use_container_width=True)
                else:
                    st.info("No Diagram Found. The AI is drawing one below...")
                    st.graphviz_chart("digraph { node[shape=record]; Chapter -> Concepts -> Exams; }")

# --- 3. EXAM FLASHCARDS (CHEAT SHEET) ---
with cheat_tab:
    if raw_text:
        col_x, col_y = st.columns(2)
        with st.spinner("Generating Flashcards..."):
            cheat_p = f"From {raw_text[:8000]}, list all FORMULAS and 5 RED-ALERT BOARD TIPS. Use format: FORMULA: [text] TIP: [text]"
            cheat_res = ai_model.generate_content(cheat_p).text
            
            with col_x:
                st.subheader("🔢 Formula Bank")
                formulas = re.findall(r'FORMULA:\s*(.*)', cheat_res)
                for f in formulas:
                    st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
            
            with col_y:
                st.subheader("🚩 Red Alert Tips")
                tips = re.findall(r'TIP:\s*(.*)', cheat_res)
                for t in tips:
                    st.markdown(f"<div class='flashcard exam-tip'><b>⚠️ Board Tip:</b><br>{t}</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("🤖 Class 10 AI Tutor v2.0")
