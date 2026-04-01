import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science AI Tutor", page_icon="🧪", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #1565C0; font-weight: bold; text-align: center; }
    .video-link { display: inline-block; background-color: #FF0000; color: white !important; 
                  padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    .bot-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
def initialize_bot():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("Please add GEMINI_KEY to Streamlit Secrets!")
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
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
        return "Error reading PDF."

# --- INTERFACE ---
st.markdown("<h1 class='main-title'>🧪 CBSE Class 10 AI Tutor & Visualizer</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Study Material")
uploaded_file = st.sidebar.file_uploader("Upload NCERT PDF Chapter", type="pdf")

if uploaded_file:
    if "syllabus_text" not in st.session_state:
        with st.spinner("Bot is reading the chapter..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Chapter Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Explain and draw 'Double Circulation' or 'A Reaction'..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Preparing your lesson..."):
                    context = st.session_state.syllabus_text[:6000]
                    
                    ai_prompt = f"""
                    You are a CBSE Class 10 Science Teacher. 
                    Context: {context}
                    Question: {prompt}
                    
                    Requirements:
                    1. Explain in simple Class 10 level language.
                    2. If a process/reaction is involved, create a simple logic flowchart using Graphviz DOT code.
                    
                    Format:
                    [Explanation Text]
                    
                    DIAGRAM_START
                    digraph G {{
                        node [shape=box, style=filled, fillcolor=lightblue];
                        "Start" -> "Next Step";
                    }}
                    DIAGRAM_END
                    
                    VIDEO_KEYWORD: [Single Topic Name]
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(ai_prompt)
                        full_res = response.text
                        
                        # PARSE TEXT, DIAGRAM, AND VIDEO
                        clean_text = full_res
                        
                        # 1. Handle Diagram Drawing
                        if "DIAGRAM_START" in full_res:
                            parts = full_res.split("DIAGRAM_START")
                            clean_text = parts[0]
                            code_and_rest = parts[1].split("DIAGRAM_END")
                            dot_code = code_and_rest[0].strip()
                            rest = code_and_rest[1] if len(code_and_rest) > 1 else ""
                            
                            st.markdown(clean_text)
                            st.subheader("📊 Concept Flowchart")
                            st.graphviz_chart(dot_code)
                            final_part = rest
                        else:
                            st.markdown(full_res)
                            final_part = full_res

                        # 2. Handle YouTube Video
                        if "VIDEO_KEYWORD:" in final_part:
                            keyword = final_part.split("VIDEO_KEYWORD:")[1].strip().split('\n')[0]
                            yt_url = f"https://www.youtube.com/results?search_query=CBSE+Class+10+Science+NCERT+{keyword.replace(' ', '+')}"
                            st.markdown(f"### 📺 Video Lesson")
                            st.markdown(f"<a href='{yt_url}' target='_blank' class='video-link'>▶️ Watch {keyword} Lesson</a>", unsafe_allow_html=True)

                        st.session_state.messages.append({"role": "assistant", "content": full_res})
                    except Exception as e:
                        st.error("AI is busy. Please try asking again in a moment!")
                        st.caption(f"Error: {e}")
            else:
                st.error("AI not configured.")

else:
    st.info("👋 To begin, upload a Science Chapter PDF from NCERT in the sidebar!")
    st.image("https://ncert.nic.in/textbook/pdf/jesc101.pdf", caption="Example: Chemical Reactions Chapter", width=200)

st.sidebar.markdown("---")
st.sidebar.caption("🎯 Syllabus: CBSE 2026-27")
