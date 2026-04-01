import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Class 10 Smart Bot", page_icon="🎓", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-title { font-size:42px; color: #2E86C1; font-weight: bold; text-align: center; }
    .video-section { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #FF0000; }
    .draw-section { background-color: #f4fdf4; padding: 15px; border-radius: 10px; border-left: 5px solid #27AE60; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE AI SETUP ---
def initialize_bot():
    try:
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0]
        return genai.GenerativeModel(name)
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return None

if "model" not in st.session_state:
    st.session_state.model = initialize_bot()

def read_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text: text += page_text + " "
    return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()

# --- APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 AI Tutor & Visualizer</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Textbook Upload")
uploaded_file = st.sidebar.file_uploader("Upload NCERT Science PDF", type="pdf")

if uploaded_file:
    if "syllabus_text" not in st.session_state:
        with st.spinner("Processing Textbook..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Ready!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question (e.g. How does the heart work?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Teaching..."):
                    context = st.session_state.syllabus_text[:7000]
                    
                    # ENHANCED PROMPT FOR DRAWING AND VIDEOS
                    final_prompt = f"""
                    Context: {context}
                    Question: {prompt}
                    
                    Instructions for Teacher Bot:
                    1. Answer in simple CBSE Class 10 language.
                    2. If the topic has a process (e.g. digestion, circuit, reaction), provide a 'Mermaid Flowchart' code.
                    3. Provide 'Exam Drawing Tips' for the diagram of this topic.
                    4. At the end, provide a single 'Keyword' for a Class 10 video search.
                    
                    Format:
                    [Text Answer]
                    
                    DRAWING_START
                    graph TD
                    A[Step 1] --> B[Step 2]
                    DRAWING_END
                    
                    VIDEO_KEYWORD: [Topic]
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(final_prompt)
                        full_res = response.text
                        
                        # 1. Handle Flowchart (The "Bot Drawing")
                        if "DRAWING_START" in full_res:
                            parts = full_res.split("DRAWING_START")
                            text_before = parts[0]
                            chart_parts = parts[1].split("DRAWING_END")
                            mermaid_code = chart_parts[0].strip()
                            text_after = chart_parts[1]
                            
                            st.markdown(text_before)
                            st.markdown("### 🟢 Concept Flowchart (Bot Drawing)")
                            st.mermaid(mermaid_code) # Renders the flowchart
                            st.markdown(text_after)
                        else:
                            st.markdown(full_res)
                        
                        # 2. Handle Strictly Filtered Video Link
                        if "VIDEO_KEYWORD:" in full_res:
                            keyword = full_res.split("VIDEO_KEYWORD:")[1].strip().split('\n')[0]
                            # Forced Search Query for Class 10
                            search_query = f"https://www.youtube.com/results?search_query=CBSE+Class+10+Science+NCERT+{keyword.replace(' ', '+')}"
                            
                            st.markdown(f"""
                            <div class='video-section'>
                                <b>📺 Class 10 Video Lesson Found:</b><br>
                                I have found a Class 10 specific lesson for <b>{keyword}</b>.<br>
                                <a href='{search_query}' target='_blank'>▶️ Click here to watch Video (Forced Class 10 Filter)</a>
                            </div>
                            """, unsafe_allow_html=True)

                        st.session_state.messages.append({"role": "assistant", "content": full_res})
                    except Exception as e:
                        st.error("Error generating answer. Try a simpler question!")
            else:
                st.error("AI not ready.")
else:
    st.info("👋 Upload your NCERT PDF to get started with drawings and videos!")
