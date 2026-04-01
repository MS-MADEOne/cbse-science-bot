import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🎓", layout="wide")

# --- 2. ADVANCED CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    .info-card { padding: 20px; border-radius: 20px; color: white; margin-bottom: 12px; min-height: 160px; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-pill { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 5px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    .video-btn { display: inline-block; background-color: #FF0000; color: white !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTO-MODEL DISCOVERY ENGINE ---
@st.cache_resource
def init_ai_bot():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Add GEMINI_KEY to Streamlit Secrets!")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # Get list of models available for YOUR key
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        # Try to pick the best one in order of preference
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
            if target in available_models:
                return genai.GenerativeModel(target)
        
        # Fallback to the first available model if targets aren't found
        return genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

ai_model = init_ai_bot()

@st.cache_data
def extract_text(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            return re.sub(r'[^\x00-\x7F]+', ' ', " ".join([p.extract_text() for p in pdf.pages])).strip()
    except: return ""

def parse_kit_data(text):
    res = {"bento": [], "formulas": [], "tips": [], "keyword": "Science"}
    lines = text.split('\n')
    for line in lines:
        clean = line.strip().replace('*', '').replace('-', '')
        if 'CONCEPT:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'APP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'EXP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FOCUS:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FORMULA:' in clean.upper(): res["formulas"].append(clean.split(':', 1)[-1].strip())
        elif 'TIP:' in clean.upper(): res["tips"].append(clean.split(':', 1)[-1].strip())
        elif 'KEYWORD:' in clean.upper(): res["keyword"] = clean.split(':', 1)[-1].strip()
    while len(res["bento"]) < 4: res["bento"].append("Study detail in textbook.")
    return res

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🚀 CBSE Class 10 Science Hub Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)

pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Session state persistency
if "kit_data" not in st.session_state: st.session_state.kit_data = None
if "active_chapter" not in st.session_state: st.session_state.active_chapter = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    
    if st.session_state.active_chapter != chapter:
        st.session_state.active_chapter = chapter
        st.session_state.kit_data = None
        st.session_state.chapter_text = extract_text(os.path.join(SYLLABUS_DIR, chapter))

    if st.sidebar.button("✨ Generate Study Kit"):
        if ai_model and st.session_state.chapter_text:
            with st.status("Tutor is analyzing content...", expanded=True) as s:
                try:
                    ctx = st.session_state.chapter_text[:5000]
                    prompt = f"Context: {ctx}. Provide: CONCEPT:, APP:, EXP:, FOCUS:, 4 FORMULA:, 4 TIP:, KEYWORD: [topic]."
                    res = ai_model.generate_content(prompt)
                    st.session_state.kit_data = parse_kit_data(res.text)
                    s.update(label="✅ Study Kit Ready!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"AI Error: {e}")
else:
    st.sidebar.warning("Upload PDFs to 'ncert_syllabus' on GitHub.")

# --- 5. TABS ---
t_chat, t_visual, t_cheat = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

with t_chat:
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Ask a question about this chapter..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            if ai_model:
                try:
                    chat_p = f"Context: {st.session_state.chapter_text[:5000]}. Q: {p}. Use DIAGRAM_START [DOT code] DIAGRAM_END for logic maps."
                    res = ai_model.generate_content(chat_p).text
                    if "DIAGRAM_START" in res:
                        st.markdown(res.split("DIAGRAM_START")[0])
                        st.graphviz_chart(res.split("DIAGRAM_START")[1].split("DIAGRAM_END")[0])
                        st.markdown(res.split("DIAGRAM_END")[1])
                    else: st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})
                except: st.error("AI Busy. Try again in 10 seconds.")

with t_visual:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        b = kit["bento"]
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div class="info-card blue-card"><b>🎯 Core Concept</b><br>{b[0]}</div>
                <div class="info-card green-card"><b>🌍 Application</b><br>{b[1]}</div>
                <div class="info-card orange-card"><b>🧪 Key Experiment</b><br>{b[2]}</div>
                <div class="info-card purple-card"><b>📈 Board Focus</b><br>{b[3]}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("🎥 **Class 10 Video Lesson**")
            kw = kit["keyword"]
            yt = f"https://www.youtube.com/results?search_query=CBSE+Class+10+NCERT+{kw.replace(' ','+')}"
            st.markdown(f"<a href='{yt}' target='_blank' class='video-btn'>▶️ Watch {kw} Video</a>", unsafe_allow_html=True)
            st.divider()
            st.graphviz_chart(f"digraph G {{ node[shape=box, style=filled, fillcolor=lightblue]; Chapter -> \"{kw}\" -> Exams; }}")
    else:
        st.info("👈 Please click **'Generate Study Kit'** in the sidebar to load.")

with t_cheat:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔢 Formulas & Equations")
            for f in kit["formulas"]: st.markdown(f"<div class='flashcard'><span class='formula-pill'>{f}</span></div>", unsafe_allow_html=True)
        with c2:
            st.subheader("🚩 Board Success Tips")
            for t in kit["tips"]: st.markdown(f"<div class='flashcard' style='border-left-color:#E74C3C;'>💡 {t}</div>", unsafe_allow_html=True)
    else:
        st.info("👈 Click **'Generate Study Kit'** to see exam flashcards.")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE Science Pro | 2026-27")
