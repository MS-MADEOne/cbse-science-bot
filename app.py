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
    .main-title { font-size:40px; color: #1E88E5; font-weight: bold; text-align: center; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UNIVERSAL AI INITIALIZATION (FIXED) ---
def get_ai_model():
    try:
        if "GEMINI_KEY" not in st.secrets:
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Standardize model selection
        model_name = "models/gemini-1.5-flash"
        try:
            m = genai.GenerativeModel(model_name)
            # Simple test to verify the key is active
            m.generate_content("test")
            return m
        except:
            return genai.GenerativeModel("gemini-pro")
    except:
        return None

if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = get_ai_model()

# --- 4. GLOBAL SCORING SEARCH ENGINE ---
def search_all_books(directory, query):
    stop_words = {"draw", "make", "explain", "show", "me", "the", "of", "and", "diagram", "please"}
    keywords = [w for w in query.lower().split() if w not in stop_words and len(w) > 2]
    
    if not keywords: keywords = query.lower().split()

    best_overall_match = {
        "score": 0,
        "text": "",
        "img": None,
        "page": 0,
        "file": ""
    }

    files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    
    for filename in files:
        path = os.path.join(directory, filename)
        doc = fitz.open(path)
        
        for page_num, page in enumerate(doc):
            text = page.get_text().lower()
            # Score based on keyword density
            score = sum(text.count(kw) for kw in keywords)
            
            if score > best_overall_match["score"]:
                best_overall_match["score"] = score
                best_overall_match["file"] = filename
                best_overall_match["page"] = page_num + 1
                
                # Extract context (3 pages)
                start = max(0, page_num - 1)
                end = min(len(doc), page_num + 2)
                context_text = ""
                for i in range(start, end):
                    context_text += doc[i].get_text() + "\n"
                best_overall_match["text"] = context_text
                
                # Take High-Res Screenshot
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                best_overall_match["img"] = Image.open(io.BytesIO(pix.tobytes()))

    return best_overall_match

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Global Science Hub</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)

# Sidebar
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])
st.sidebar.title("📚 Library Hub")
st.sidebar.success(f"Chapters Loaded: {len(pdf_files)}")

# Chat History
if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "image" in m and m["image"]: st.image(m["image"])
        if "graph" in m and m["graph"]: st.graphviz_chart(m["graph"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask: 'Draw Human Eye' or 'Explain Oxidation'..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Scanning entire Library for the best match..."):
            match = search_all_books(SYLLABUS_DIR, prompt)

        if match["score"] > 0:
            if st.session_state.ai_brain:
                try:
                    # Specialized prompt for 'Draw' requests
                    ai_prompt = f"""
                    You are a CBSE Science Teacher. Use this NCERT data: {match['text'][:5000]}
                    Student Question: {prompt}
                    Instruction: 
                    1. Explain in simple Class 10 terms.
                    2. If asked to 'draw', create a logic flowchart using DOT code.
                    Format: [Answer] DIAGRAM_START [DOT code] DIAGRAM_END
                    """
                    response = st.session_state.ai_brain.generate_content(ai_prompt)
                    ans_text = response.text
                    
                    # Handle AI Drawing (Graphviz)
                    graph_code = ""
                    if "DIAGRAM_START" in ans_text:
                        parts = ans_text.split("DIAGRAM_START")
                        ans_text = parts[0]
                        graph_code = parts[1].split("DIAGRAM_END")[0].strip()

                    final_res = f"{ans_text}\n\n**📍 Source: {match['file']} (Page {match['page']})**"
                    st.markdown(final_res)
                    
                    if graph_code:
                        st.subheader("📊 Logic Flowchart (Bot Drawing)")
                        st.graphviz_chart(graph_code)
                    
                    if match["img"]:
                        st.subheader("🖼️ Textbook Reference Page")
                        st.image(match["img"])
                    
                    st.session_state.history.append({
                        "role": "assistant", 
                        "content": final_res, 
                        "image": match["img"], 
                        "graph": graph_code
                    })
                except Exception as e:
                    st.error("AI is temporarily unavailable. Here is the textbook page:")
                    st.image(match["img"])
            else:
                st.warning(f"Found in {match['file']} (Page {match['page']}), but AI key is missing.")
                st.image(match["img"])
        else:
            st.error("❌ Topic not found. Please ensure all Science PDFs are in the 'ncert_syllabus' folder.")

st.sidebar.markdown("---")
st.sidebar.caption("CBSE 2026-27 | Digital Tutor")
