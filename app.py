import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
import re
import os
import io

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Master Pro", page_icon="🧪", layout="wide")

# --- 2. STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    .info-card { padding: 20px; border-radius: 20px; color: white; margin-bottom: 12px; min-height: 140px; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI INITIALIZATION ---
@st.cache_resource
def init_ai():
    try:
        if "GEMINI_KEY" not in st.secrets: return None, "❌ Key Missing"
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Use gemini-1.5-flash: It's the most stable for free-tier quotas
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model, "✅ AI Brain Ready"
    except: return None, "⚠️ AI Offline"

if "ai_brain" not in st.session_state:
    st.session_state.ai_brain, st.session_state.ai_status = init_ai()

# --- 4. SMART GLOBAL SEARCH ---
def global_search(query, directory):
    keywords = [w for w in query.lower().split() if len(w) > 2]
    best_match = {"score": 0, "text": "", "img": None, "page": 0, "file": ""}
    if not os.path.exists(directory): return best_match
    
    for filename in os.listdir(directory):
        if not filename.endswith(".pdf"): continue
        doc = fitz.open(os.path.join(directory, filename))
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            score = sum(text.count(kw) for kw in keywords)
            if score > best_match["score"]:
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                best_match.update({
                    "score": score, "file": filename, "page": page_num + 1,
                    "text": page.get_text(), "img": Image.open(io.BytesIO(pix.tobytes()))
                })
    return best_match

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Hub Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if "history" not in st.session_state: st.session_state.history = []
if "kit_data" not in st.session_state: st.session_state.kit_data = {}

st.sidebar.title("🤖 AI Status")
st.sidebar.info(st.session_state.ai_status)

# --- TABS ---
t_chat, t_visual, t_cheat = st.tabs(["💬 Smart AI Tutor", "🖼️ Visual Dashboard", "⚡ Exam Flashcards"])

# TAB 1: SMART TUTOR
with t_chat:
    for m in st.session_state.history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "graph" in m and m["graph"]: st.graphviz_chart(m["graph"])
            if "image" in m and m["image"]: st.image(m["image"], caption="Textbook Reference")

    if prompt := st.chat_input("Ask: 'Explain respiration with a diagram' or 'Properties of acids'"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            match = global_search(prompt, SYLLABUS_DIR)
            if match["score"] > 0:
                try:
                    with st.spinner("AI is analyzing and drawing..."):
                        # ONE CALL PROMPT: Asks for Answer, Infographics, and Flashcards in one go
                        mega_prompt = f"""
                        Context: {match['text'][:4000]}
                        Question: {prompt}
                        
                        You are a CBSE Science Teacher. Provide a response in this EXACT format:
                        ANSWER: [Your smart, helpful explanation here]
                        
                        DIAGRAM: [If a process exists, provide a simple Graphviz DOT flowchart code here, else leave empty]
                        
                        INFOGRAPHIC:
                        CONCEPT: [One line]
                        APP: [One line]
                        EXP: [One line]
                        FOCUS: [One line]
                        
                        FLASHCARDS:
                        FORMULA: [List 3-4]
                        TIP: [List 3-4]
                        """
                        response = st.session_state.ai_brain.generate_content(mega_prompt).text
                        
                        # PARSING THE MEGA RESPONSE
                        answer = response.split("ANSWER:")[1].split("DIAGRAM:")[0].strip()
                        diagram = response.split("DIAGRAM:")[1].split("INFOGRAPHIC:")[0].strip()
                        infographic = response.split("INFOGRAPHIC:")[1].split("FLASHCARDS:")[0].strip()
                        flashcards = response.split("FLASHCARDS:")[1].strip()

                        final_ans = f"{answer}\n\n**📍 Source: {match['file']} (Page {match['page']})**"
                        st.markdown(final_ans)
                        
                        # Show Diagram if AI generated one
                        graph_code = ""
                        if "digraph" in diagram:
                            graph_code = diagram
                            st.graphviz_chart(graph_code)
                        
                        st.image(match["img"], caption="Textbook Reference Page")

                        # SAVE TO SESSION FOR OTHER TABS (SAVES QUOTA!)
                        st.session_state.kit_data = {
                            "bento": [l.split(':', 1)[-1].strip() for l in infographic.split('\n') if ':' in l],
                            "formulas": [l.split(':', 1)[-1].strip() for l in flashcards.split('\n') if 'FORMULA:' in l.upper()],
                            "tips": [l.split(':', 1)[-1].strip() for l in flashcards.split('\n') if 'TIP:' in l.upper()]
                        }
                        
                        st.session_state.history.append({
                            "role": "assistant", "content": final_ans, 
                            "image": match["img"], "graph": graph_code
                        })

                except Exception as e:
                    if "429" in str(e): st.error("🚦 Quota Limit! Please wait 60 seconds.")
                    else: st.error(f"Error: {e}")
            else:
                st.warning("Topic not found. Try keywords like 'Eye', 'Heart', 'Acids'.")

# TAB 2: VISUAL DASHBOARD
with t_visual:
    if st.session_state.kit_data:
        pts = st.session_state.kit_data["bento"]
        while len(pts) < 4: pts.append("Refer to textbook.")
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="info-card blue-card"><b>🎯 Concept</b><br>{pts[0]}</div>
            <div class="info-card green-card"><b>🌍 Application</b><br>{pts[1]}</div>
            <div class="info-card orange-card"><b>🧪 Experiment</b><br>{pts[2]}</div>
            <div class="info-card purple-card"><b>📈 Board Focus</b><br>{pts[3]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Ask a question in the **Smart AI Tutor** tab to see visuals!")

# TAB 3: EXAM FLASHCARDS
with t_cheat:
    if st.session_state.kit_data:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔢 Formulas & Equations")
            for f in st.session_state.kit_data["formulas"]:
                st.markdown(f"<div class='flashcard'><span class='formula-tag'>{f}</span></div>", unsafe_allow_html=True)
        with c2:
            st.subheader("🚩 Board Success Tips")
            for t in st.session_state.kit_data["tips"]:
                st.markdown(f"<div class='flashcard' style='border-left-color:#E74C3C;'>💡 {t}</div>", unsafe_allow_html=True)
    else:
        st.info("Ask a question in the **Smart AI Tutor** tab to see flashcards!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE Science Pro | One-Call Mode")
