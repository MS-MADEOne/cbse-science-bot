import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Class 10th Science AI Tutor", page_icon="🎓", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:38px; color: #1565C0; font-weight: bold; text-align: center; }
    .video-link { display: inline-block; background-color: #FF0000; color: white !important; 
                  padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SMART MODEL SELECTION ---
def initialize_bot():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Missing GEMINI_KEY in Secrets!")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # This scans all models available to YOUR API key
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        # Pick the best one available (Flash > Pro > Any)
        target_models = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        final_model_name = next((m for m in target_models if m in available_models), available_models[0])
        
        return genai.GenerativeModel(final_model_name)
    except Exception as e:
        st.error(f"Initialization Failed: {e}")
        return None

if "model" not in st.session_state:
    st.session_state.model = initialize_bot()

def read_pdf(file):
    try:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text: text += page_text + " "
        return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()
    except:
        return ""

# --- APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 AI Tutor & Drawer</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Study Material")
uploaded_file = st.sidebar.file_uploader("Upload NCERT PDF Chapter", type="pdf")

if uploaded_file:
    if "syllabus_text" not in st.session_state:
        with st.spinner("Bot is reading the PDF..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Chapter Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Explain and draw 'Double Circulation' or 'A Reaction'..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Tutor is thinking..."):
                    # Use a part of the textbook for context
                    context = st.session_state.syllabus_text[:6000] if "syllabus_text" in st.session_state else ""
                    
                    ai_prompt = f"""
                    You are a CBSE Class 10 Science Teacher. 
                    Context: {context}
                    Question: {prompt}
                    
                    Instructions:
                    1. Use simple Class 10 Board language.
                    2. For any process or reaction, draw a flowchart using Graphviz DOT code.
                    
                    Format:
                    [Your Answer]
                    
                    DIAGRAM_START
                    digraph G {{
                        node [shape=box, style=filled, fillcolor=lightblue];
                        "Reactants" -> "Products";
                    }}
                    DIAGRAM_END
                    
                    VIDEO_KEYWORD: [Topic Name]
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(ai_prompt)
                        full_res = response.text
                        
                        # PARSE LOGIC
                        if "DIAGRAM_START" in full_res:
                            parts = full_res.split("DIAGRAM_START")
                            st.markdown(parts[0])
                            
                            code_rest = parts[1].split("DIAGRAM_END")
                            dot_code = code_rest[0].strip()
                            st.subheader("📊 Concept Flowchart")
                            st.graphviz_chart(dot_code)
                            
                            final_part = code_rest[1] if len(code_rest) > 1 else ""
                        else:
                            st.markdown(full_res)
                            final_part = full_res

                        if "VIDEO_KEYWORD:" in final_part:
                            keyword = final_part.split("VIDEO_KEYWORD:")[1].strip().split('\n')[0]
                            yt_url = f"https://www.youtube.com/results?search_query=CBSE+Class+10+Science+NCERT+{keyword.replace(' ', '+')}"
                            st.markdown(f"### 📺 Video Lesson")
                            st.markdown(f"<a href='{yt_url}' target='_blank' class='video-link'>▶️ Watch {keyword} Lesson</a>", unsafe_allow_html=True)

                        st.session_state.messages.append({"role": "assistant", "content": full_res})
                    except Exception as e:
                        st.error("I'm having trouble connecting to the AI. Let's try again.")
                        st.caption(f"Technical Log: {e}")
            else:
                st.error("AI is currently unavailable.")

else:
    st.info("👋 To begin, upload a Science Chapter PDF from NCERT in the sidebar!")
