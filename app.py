import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="CBSE Science Hub Pro", page_icon="🧪", layout="wide")

# --- 2. STYLING (Bento Grids & Flashcards) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    
    /* Bento Cards */
    .info-card { padding: 20px; border-radius: 18px; color: white; margin-bottom: 12px; min-height: 140px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    
    /* Flashcards */
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI & PDF ENGINES ---
@st.cache_resource
def init_ai_engine():
    try:
        if "GEMINI_KEY" not in st.secrets: return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Attempt to find the best available model
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0]
        return genai.GenerativeModel(name)
    except: return None

ai_model = init_ai_engine()

@st.cache_data
def get_clean_text(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            text = " ".join([page.extract_text() for page in pdf.pages])
            return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()
    except: return ""

def get_wiki_img(q):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={q}"
        return requests.get(url).json()['query']['pages'][0]['original']['source']
    except: return None

# --- 4. ROBUST KEYWORD PARSER ---
def parse_study_kit(text):
    """Parses AI response by looking for specific keywords/labels"""
    sections = {"bento": [], "formulas": [], "tips": []}
    lines = text.split('\n')
    
    for line in lines:
        clean = line.strip().replace('- ', '').replace('* ', '')
        if 'CONCEPT:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'APP:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'EXP:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FOCUS:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FORMULA:' in clean.upper(): sections["formulas"].append(clean.split(':', 1)[-1].strip())
        elif 'TIP:' in clean.upper(): sections["tips"].append(clean.split(':', 1)[-1].strip())
    
    # Fill gaps to prevent UI empty boxes
    while len(sections["bento"]) < 4: sections["bento"].append("Refer to NCERT textbook for more details.")
    return sections

# --- 5. MAIN APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Initialize Session States for Persistence
if "kit_data" not in st.session_state: st.session_state.kit_data = None
if "current_chap" not in st.session_state: st.session_state.current_chap = None
if "msgs" not in st.session_state: st.session_state.msgs = []

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    
    # Reset if chapter changes
    if st.session_state.current_chap != chapter:
        st.session_state.current_chap = chapter
        st.session_state.kit_data = None
        st.session_state.raw_text = get_clean_text(os.path.join(SYLLABUS_DIR, chapter))

    # PERSISTENT GENERATE BUTTON
    if st.sidebar.button("✨ Generate Visual Study Kit"):
        if ai_model and st.session_state.raw_text:
            with st.status("Tutor is analyzing chapter...", expanded=True) as status:
                st.write("Extracting key concepts...")
                prompt = f"""
                Analyze the following Science content: {st.session_state.raw_text[:6000]}
                Provide exactly these labels followed by a colon:
                CONCEPT: [One line summary]
                APP: [One real life application]
                EXP: [One key experiment]
                FOCUS: [One important exam topic]
                FORMULA: [List 4 major formulas or equations]
                TIP: [List 4 board exam tips]
                """
                try:
                    response = ai_model.generate_content(prompt)
                    st.session_state.kit_data = parse_study_kit(response.text)
                    status.update(label="✅ Study Kit Ready!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"AI Error: {e}")
        else:
            st.sidebar.error("AI or PDF not ready.")
else:
    st.sidebar.warning("Upload PDFs to 'ncert_syllabus' folder on GitHub!")
    st.stop()

# --- 6. TABS SYSTEM ---
chat_tab, info_tab, cheat_tab = st.tabs(["💬 AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

# TAB 1: CHAT
with chat_tab:
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Ask a question about this chapter..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            if ai_model:
                try:
                    res = ai_model.generate_content(f"Context: {st.session_state.raw_text[:5000]}. Question: {p}").text
                    st.markdown(res)
                    st.session_state.msgs.append({"role": "assistant", "content": res})
                except: st.error("AI is temporarily overloaded. Please wait.")

# TAB 2: VISUAL INFOGRAPHICS
with info_tab:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        b = kit["bento"]
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div class="info-card blue-card"><b>🎯 Core Concept</b><br>{b[0]}</div>
                <div class="info-card green-card"><b>🌍 Application</b><br>{b[1]}</div>
                <div class="info-card orange-card"><b>🧪 Key Experiment</b><br>{b[2]}</div>
                <div class="info-card purple-card"><b>📈 Board Focus</b><br>{b[3]}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("📸 **Diagram Reference**")
            term = chapter.replace(".pdf", "").split("_")[-1]
            img = get_wiki_img(term)
            if img: st.image(img, use_container_width=True)
            else: st.info("Check NCERT textbook for visual diagrams.")
    else:
        st.info("👈 Please click **'Generate Visual Study Kit'** in the sidebar to load infographics.")

# TAB 3: EXAM FLASHCARDS
with cheat_tab:
    if st.session_state.kit_data:
        kit = st.session_state.kit_data
        cx, cy = st.columns(2)
        with cx:
            st.subheader("🔢 Formulas & Equations")
            if kit["formulas"]:
                for f in kit["formulas"]: 
                    st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
            else: st.write("No specific formulas found.")
        with cy:
            st.subheader("🚩 Red Alert Board Tips")
            if kit["tips"]:
                for t in kit["tips"]: 
                    st.markdown(f"<div class='flashcard' style='border-left-color:#E74C3C;'>💡 {t}</div>", unsafe_allow_html=True)
            else: st.write("General NCERT study recommended.")
    else:
        st.info("👈 Please click **'Generate Visual Study Kit'** in the sidebar to load flashcards.")

st.sidebar.markdown("---")
st.sidebar.caption("🤖 Powered by Google Gemini | CBSE 2026-27")
