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
    .main-title { font-size:42px; color: #1E88E5; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .status-box { padding: 10px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ROBUST AI INITIALIZATION ---
def init_ai():
    try:
        if "GEMINI_KEY" not in st.secrets:
            return None, "❌ API Key Missing in Secrets"
        
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # Try finding the best available model
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # We prefer gemini-1.5-flash as it is the most stable for PDF context
        model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else "models/gemini-pro"
        
        model = genai.GenerativeModel(model_name)
        # Test connection
        model.generate_content("test")
        return model, "✅ AI Brain Connected"
    except Exception as e:
        return None, f"⚠️ AI Offline: {str(e)[:50]}"

# Initialize AI in session state
if "ai_brain" not in st.session_state:
    st.session_state.ai_brain, st.session_state.ai_status = init_ai()

# --- 4. SMART SEARCH ENGINE ---
def search_books(directory, query):
    # Filter out common words to focus on science terms
    stop_words = {"draw", "show", "me", "the", "and", "diagram", "please", "make", "explain"}
    keywords = [w for w in query.lower().split() if w not in stop_words and len(w) > 2]
    if not keywords: keywords = query.lower().split()

    best_match = {"score": 0, "text": "", "img": None, "page": 0, "file": ""}
    
    files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    
    for filename in files:
        doc = fitz.open(os.path.join(directory, filename))
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            score = sum(text.count(kw) for kw in keywords)
            
            if score > best_match["score"]:
                best_match.update({
                    "score": score, "file": filename, "page": page_num + 1,
                    "text": page.get_text(), # Only current page text to keep it light
                    "img": Image.open(io.BytesIO(page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes()))
                })
    return best_match

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

# Sidebar Status
SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)

st.sidebar.title("🤖 Assistant Status")
st.sidebar.markdown(f"**AI Engine:** {st.session_state.ai_status}")
if st.sidebar.button("♻️ Reconnect AI"):
    st.session_state.ai_brain, st.session_state.ai_status = init_ai()
    st.rerun()

# Chat History
if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m and m["image"]: st.image(m["image"])
        if "graph" in m and m["graph"]: st.graphviz_chart(m["graph"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Search: 'Draw Human Eye' or 'Explain Electricity'..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching NCERT Library..."):
            match = search_books(SYLLABUS_DIR, prompt)

        if match["score"] > 0:
            if st.session_state.ai_brain:
                try:
                    # Very specific prompt to ensure AI generates Graphviz DOT code
                    ai_prompt = f"""
                    Context: {match['text'][:3000]}
                    Question: {prompt}
                    Role: CBSE Science Teacher
                    Task: 
                    1. Short explanation.
                    2. If 'draw' is asked, provide a logic flowchart using DOT language.
                    Format: [Answer] DIAGRAM_START [DOT code] DIAGRAM_END
                    """
                    response = st.session_state.ai_brain.generate_content(ai_prompt)
                    res_text = response.text
                    
                    graph_code = ""
                    if "DIAGRAM_START" in res_text:
                        parts = res_text.split("DIAGRAM_START")
                        res_text = parts[0]
                        graph_code = parts[1].split("DIAGRAM_END")[0].strip()

                    final_msg = f"{res_text}\n\n**📍 Source: {match['file']} (Page {match['page']})**"
                    st.markdown(final_msg)
                    
                    if graph_code:
                        st.subheader("📊 Logic Flowchart (Bot Drawing)")
                        st.graphviz_chart(graph_code)
                    
                    st.subheader("🖼️ Textbook Page Reference")
                    st.image(match["img"])
                    
                    st.session_state.history.append({
                        "role": "assistant", "content": final_msg, 
                        "image": match["img"], "graph": graph_code
                    })
                except Exception as e:
                    st.error(f"AI Limit Reached (Error 429). Please wait 30s. Here is the textbook page for now:")
                    st.image(match["img"])
            else:
                st.warning(f"AI Brain not connected, but I found this in {match['file']}:")
                st.image(match["img"])
        else:
            st.error("❌ Topic not found in NCERT files. Try simpler keywords!")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE 2026-27 | Digital Tutor")
