import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
import re
import os
import io
import requests

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Master Pro", page_icon="🧪", layout="wide")

# --- 2. ADVANCED STYLING (Bento & Flashcards) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    
    /* Bento Grid */
    .info-card { padding: 20px; border-radius: 20px; color: white; margin-bottom: 12px; min-height: 150px; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    
    /* Flashcards */
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTO-MODEL DISCOVERY ENGINE (FIXES 404) ---
@st.cache_resource
def init_ai():
    try:
        if "GEMINI_KEY" not in st.secrets: return None, "❌ Key Missing"
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in ["models/gemini-1.5-flash", "models/gemini-pro"] if m in available), available[0])
        model = genai.GenerativeModel(target)
        model.generate_content("Hi") # Test
        return model, f"✅ Connected to {target.split('/')[-1]}"
    except Exception as e: return None, f"⚠️ AI Offline: {str(e)[:40]}"

if "ai_brain" not in st.session_state:
    st.session_state.ai_brain, st.session_state.ai_status = init_ai()

# --- 4. GLOBAL SEARCH ENGINE (High-Res Diagrams) ---
def global_search(query, directory):
    stop_words = {"draw", "show", "me", "diagram", "please", "explain", "the", "and"}
    keywords = [w for w in query.lower().split() if w not in stop_words and len(w) > 2]
    if not keywords: keywords = query.lower().split()
    
    best_match = {"score": 0, "text": "", "img": None, "page": 0, "file": ""}
    if not os.path.exists(directory): return best_match
    
    for filename in os.listdir(directory):
        if not filename.endswith(".pdf"): continue
        doc = fitz.open(os.path.join(directory, filename))
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            score = sum(text.count(kw) for kw in keywords)
            if score > best_match["score"]:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                best_match.update({
                    "score": score, "file": filename, "page": page_num + 1,
                    "text": page.get_text(), "img": Image.open(io.BytesIO(pix.tobytes()))
                })
    return best_match

# --- 5. MAIN APP ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Master Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if "history" not in st.session_state: st.session_state.history = []
if "kit_data" not in st.session_state: st.session_state.kit_data = None

# Sidebar
st.sidebar.title("🤖 AI Status")
st.sidebar.info(st.session_state.ai_status)
if st.sidebar.button("♻️ Reset Connection"):
    st.session_state.ai_brain, st.session_state.ai_status = init_ai()
    st.rerun()

# --- TABS SYSTEM ---
t_chat, t_visual, t_cheat = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

# TAB 1: AI TUTOR
with t_chat:
    for m in st.session_state.history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "image" in m and m["image"]: st.image(m["image"])
            if "graph" in m and m["graph"]: st.graphviz_chart(m["graph"])

    if prompt := st.chat_input("Ask: 'Draw Human Eye' or 'Explain Oxidation'..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            match = global_search(prompt, SYLLABUS_DIR)
            if match["score"] > 0:
                try:
                    ai_prompt = f"Context: {match['text'][:3000]}. Question: {prompt}. If 'draw' is asked, generate DOT code. Format: [Text] DIAGRAM_START [DOT Code] DIAGRAM_END"
                    res = st.session_state.ai_brain.generate_content(ai_prompt).text
                    
                    graph_code = ""
                    if "DIAGRAM_START" in res:
                        parts = res.split("DIAGRAM_START")
                        res = parts[0]
                        graph_code = parts[1].split("DIAGRAM_END")[0].strip()
                    
                    final_res = f"{res}\n\n**📍 Source: {match['file']} (Page {match['page']})**"
                    st.markdown(final_res)
                    if graph_code: st.graphviz_chart(graph_code)
                    st.image(match["img"], caption="Textbook Reference Diagram")
                    
                    st.session_state.history.append({"role": "assistant", "content": final_res, "image": match["img"], "graph": graph_code})
                    st.session_state.last_context = match['text'] # Store for visuals
                except Exception as e:
                    st.error(f"AI Busy. Showing textbook page: {e}")
                    st.image(match["img"])
            else:
                st.warning("Topic not found in ncert_syllabus folder.")

# TAB 2: VISUAL DASHBOARD (INFOGRAPHICS)
with t_visual:
    if "last_context" in st.session_state:
        if st.button("✨ Generate Visual Infographics for this Topic"):
            with st.spinner("Creating Bento Grid..."):
                try:
                    p = f"Summarize this: {st.session_state.last_context[:4000]} into 4 labels: CONCEPT:, APP:, EXP:, FOCUS:."
                    res = st.session_state.ai_brain.generate_content(p).text
                    # Simple parsing
                    lines = res.split('\n')
                    pts = [l.split(':', 1)[-1] for l in lines if ':' in l]
                    while len(pts) < 4: pts.append("Refer to textbook.")
                    
                    st.markdown(f"""
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div class="info-card blue-card"><b>🎯 Concept</b><br>{pts[0]}</div>
                        <div class="info-card green-card"><b>🌍 Application</b><br>{pts[1]}</div>
                        <div class="info-card orange-card"><b>🧪 Experiment</b><br>{pts[2]}</div>
                        <div class="info-card purple-card"><b>📈 Weightage</b><br>{pts[3]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except: st.error("AI Limit hit. Try in 1 minute.")
    else: st.info("Search for a topic in the AI Tutor tab first!")

# TAB 3: EXAM FLASHCARDS
with t_cheat:
    if "last_context" in st.session_state:
        if st.button("⚡ Generate Exam Flashcards"):
            with st.spinner("Writing Flashcards..."):
                try:
                    p = f"List 4 FORMULAS and 4 TIPS from: {st.session_state.last_context[:4000]}"
                    res = st.session_state.ai_brain.generate_content(p).text
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🔢 Formulas")
                        for f in re.findall(r'FORMULA:\s*(.*)', res): st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
                    with c2:
                        st.subheader("🚩 Board Tips")
                        for t in re.findall(r'TIP:\s*(.*)', res): st.markdown(f"<div class='flashcard' style='border-left-color:red;'>{t}</div>", unsafe_allow_html=True)
                except: st.info("Ask a specific question to generate flashcards.")
    else: st.info("Search for a topic in the AI Tutor tab first!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE Science Pro v3.0 | 2026-27")
