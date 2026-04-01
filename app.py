import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🧪", layout="wide")

# --- 2. STYLING (KEEPING IT BEAUTIFUL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    .info-card { padding: 20px; border-radius: 18px; color: white; margin-bottom: 12px; min-height: 140px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ROBUST AI INITIALIZATION ---
def get_ai_model():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("🔑 API Key not found! Add 'GEMINI_KEY' in Streamlit Secrets.")
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # We use gemini-1.5-flash as it's the most reliable for Free Tier
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

# Load the model into session state so it persists
if "model_engine" not in st.session_state:
    st.session_state.model_engine = get_ai_model()

# --- 4. DATA PROCESSING ---
@st.cache_data
def load_text_from_pdf(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            return " ".join([p.extract_text() for p in pdf.pages])
    except: return ""

def parse_kit_output(text):
    """Parses AI output by looking for specific labels"""
    res = {"bento": [], "formulas": [], "tips": []}
    lines = text.split('\n')
    for line in lines:
        clean = line.strip().replace('*', '').replace('-', '')
        if 'CONCEPT:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'APP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'EXP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FOCUS:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FORMULA:' in clean.upper(): res["formulas"].append(clean.split(':', 1)[-1].strip())
        elif 'TIP:' in clean.upper(): res["tips"].append(clean.split(':', 1)[-1].strip())
    
    # Fill defaults if AI skipped something
    while len(res["bento"]) < 4: res["bento"].append("Refer to NCERT textbook.")
    return res

# --- 5. MAIN APP ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR):
    st.info("Please create a folder 'ncert_syllabus' on GitHub and upload PDFs.")
    st.stop()

pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Session state initialization
if "kit_data" not in st.session_state: st.session_state.kit_data = None
if "active_chapter" not in st.session_state: st.session_state.active_chapter = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Choose Chapter", pdf_files)
    
    # Handle chapter change
    if st.session_state.active_chapter != chapter:
        st.session_state.active_chapter = chapter
        st.session_state.kit_data = None # Reset kit for new chapter
        st.session_state.chapter_text = load_text_from_pdf(os.path.join(SYLLABUS_DIR, chapter))

    # GENERATE BUTTON
    if st.sidebar.button("✨ Generate Visual Study Kit"):
        if st.session_state.model_engine and st.session_state.chapter_text:
            with st.spinner("Analyzing Textbook..."):
                try:
                    # Shorter context to avoid 400 errors
                    context = st.session_state.chapter_text[:5000]
                    prompt = f"Using this text: {context}. Give: CONCEPT:, APP:, EXP:, FOCUS:, 4 FORMULA:, 4 TIP:."
                    response = st.session_state.model_engine.generate_content(prompt)
                    st.session_state.kit_data = parse_kit_output(response.text)
                    st.sidebar.success("Kit Ready! Switch tabs to view.")
                except Exception as e:
                    st.sidebar.error(f"AI Error: {e}")
        else:
            st.sidebar.warning("AI not ready or PDF empty.")

# --- 6. TABS ---
tab_chat, tab_visual, tab_cheat = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

with tab_chat:
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Ask a question about this chapter..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            if st.session_state.model_engine:
                try:
                    ctx = st.session_state.chapter_text[:4000]
                    res = st.session_state.model_engine.generate_content(f"Context: {ctx}. Q: {p}").text
                    st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})
                except Exception as e: st.error(f"Chat Error: {e}")

with tab_visual:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        b = kit["bento"]
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div class="info-card blue-card"><b>🎯 Core Concept</b><br>{b[0]}</div>
            <div class="info-card green-card"><b>🌍 Application</b><br>{b[1]}</div>
            <div class="info-card orange-card"><b>🧪 Key Experiment</b><br>{b[2]}</div>
            <div class="info-card purple-card"><b>📈 Board Focus</b><br>{b[3]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("👈 Please click **'Generate Visual Study Kit'** in the sidebar to see visuals.")

with tab_cheat:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔢 Formula Bank")
            for f in kit["formulas"]: st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
        with c2:
            st.subheader("🚩 Board Tips")
            for t in kit["tips"]: st.markdown(f"<div class='flashcard' style='border-left-color:#E74C3C;'>💡 {t}</div>", unsafe_allow_html=True)
    else:
        st.info("👈 Please click **'Generate Visual Study Kit'** in the sidebar to see flashcards.")
