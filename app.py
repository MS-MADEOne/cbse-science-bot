import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science Smart Tutor", page_icon="🧪", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #1565C0; font-weight: bold; text-align: center; }
    .bot-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; }
    .video-link { color: #ffffff !important; background-color: #FF0000; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
def initialize_bot():
    try:
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        # Use 1.5-flash for speed and logic
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error("API Key not found in Secrets!")
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

# --- INTERFACE ---
st.markdown("<h1 class='main-title'>🧪 CBSE Class 10 Science AI Tutor</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Study Room")
uploaded_file = st.sidebar.file_uploader("Upload NCERT PDF (Chemistry/Bio/Physics)", type="pdf")

if uploaded_file:
    if "syllabus_text" not in st.session_state:
        with st.spinner("Bot is reading your textbook..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me to explain or 'draw' a concept..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Tutor is preparing your lesson..."):
                    context = st.session_state.syllabus_text[:6000]
                    
                    # STRICT PROMPT FOR GRAPHVIZ DRAWING
                    final_prompt = f"""
                    You are a CBSE Class 10 Science Teacher. 
                    Textbook Context: {context}
                    Question: {prompt}
                    
                    Instructions:
                    1. Explain in clear Class 10 Board level language.
                    2. If asked to 'draw' or if the concept is a process, provide a logic-map using DOT language (Graphviz).
                    
                    Format your response EXACTLY like this:
                    [Detailed Explanation]
                    
                    DIAGRAM_START
                    digraph G {{
                      node [shape=box, style=filled, fillcolor=lightblue];
                      "Reactant A" -> "Product B" [label="Heat"];
                    }}
                    DIAGRAM_END
                    
                    VIDEO_KEYWORD: [Single word for video search]
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(final_prompt)
                        full_res = response.text
                        
                        # PARSING THE RESPONSE
                        main_text = full_res
                        
                        # 1. Extract and Draw Diagram
                        if "DIAGRAM_START" in full_res:
                            main_text = full_res.split("DIAGRAM_START")[0]
                            diagram_code = full_res.split("DIAGRAM_START")[1].split("DIAGRAM_END")[0].strip()
                            st.markdown(main_text)
                            st.subheader("📊 Concept Visualization")
                            st.grap
