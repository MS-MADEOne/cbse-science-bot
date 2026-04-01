import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science Smart Library", page_icon="📚", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:38px; color: #1565C0; font-weight: bold; text-align: center; }
    .video-link { display: inline-block; background-color: #FF0000; color: white !important; 
                  padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    .lib-box { background-color: #f1f8ff; padding: 10px; border-radius: 8px; border-left: 5px solid #1565C0; }
    </style>
    """, unsafe_allow_html=True)

# --- SMART MODEL SELECTION ---
@st.cache_resource
def initialize_bot():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Missing GEMINI_KEY in Secrets!")
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_models = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        final_model_name = next((m for m in target_models if m in available_models), available_models[0])
        return genai.GenerativeModel(final_model_name)
    except:
        return None

model = initialize_bot()

# --- PDF PROCESSING ---
@st.cache_data
def load_built_in_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            pdf_reader = pypdf.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text: text += page_text + " "
            return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()
    except Exception as e:
        return f"Error loading file: {e}"

# --- APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Digital Science Library</h1>", unsafe_allow_html=True)

# SIDEBAR: CHAPTER SELECTION
st.sidebar.title("📖 Chapter Library")

# THIS IS THE LINE YOU WERE LOOKING FOR:
SYLLABUS_DIR = "ncert_syllabus" 

# Create the folder if it doesn't exist yet
if not os.path.exists(SYLLABUS_DIR):
    os.makedirs(SYLLABUS_DIR)

# Get list of PDF files
pdf_files = [f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")]

if pdf_files:
    selected_file = st.sidebar.selectbox("📂 Select a Chapter to Study:", pdf_files)
    file_path = os.path.join(SYLLABUS_DIR, selected_file)
    
    # Load text automatically
    syllabus_text = load_built_in_pdf(file_path)
    st.sidebar.success(f"Loaded: {selected_file}")
else:
    st.sidebar.warning(f"No PDFs found in '{SYLLABUS_DIR}' folder.")
    syllabus_text = ""

# CHAT INTERFACE
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about this chapter..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            with st.spinner("Tutor is searching the textbook..."):
                context = syllabus_text[:8000] if syllabus_text else ""
                
                ai_prompt = f"""
                You are a CBSE Class 10 Science Teacher. 
                Context: {context}
                Question: {prompt}
                Instructions: Answer in Class 10 language. 
                If a process/reaction is involved, draw a flowchart using Graphviz DOT code.
                Format: [Answer] DIAGRAM_START [DOT Code] DIAGRAM_END VIDEO_KEYWORD: [Topic]
                """
                
                try:
                    response = model.generate_content(ai_prompt)
                    full_res = response.text
                    
                    if "DIAGRAM_START" in full_res:
                        parts = full_res.split("DIAGRAM_START")
                        st.markdown(parts[0])
                        code_rest = parts[1].split("DIAGRAM_END")
                        st.graphviz_chart(code_rest[0].strip())
                        final_text = code_rest[1] if len(code_rest) > 1 else ""
                    else:
                        st.markdown(full_res)
                        final_text = full_res

                    if "VIDEO_KEYWORD:" in final_text:
                        keyword = final_text.split("VIDEO_KEYWORD:")[1].strip().split('\n')[0]
                        yt_url = f"https://www.youtube.com/results?search_query=CBSE+Class+10+Science+NCERT+{keyword.replace(' ', '+')}"
                        st.markdown(f"### 📺 Video Lesson\n<a href='{yt_url}' target='_blank' class='video-link'>▶️ Watch {keyword} Lesson</a>", unsafe_allow_html=True)

                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error("Connection Error. Please try again.")
        else:
            st.error("AI Key Error. Check Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.caption("Syllabus: CBSE 2026-27")
