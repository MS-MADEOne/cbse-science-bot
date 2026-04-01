import streamlit as st
import pypdf
import google.generativeai as genai

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science AI Tutor", page_icon="🧬", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #1E88E5; font-weight: bold; text-align: center; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE AI SETUP ---
# For security, you can put your key here, OR use Streamlit Secrets
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def read_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- APP INTERFACE ---
st.markdown('<p class="main-title">🤖 CBSE Class 10 Smart AI Tutor</p>', unsafe_allow_html=True)

st.sidebar.title("📚 Study Material")
uploaded_file = st.sidebar.file_uploader("Upload NCERT Science PDF", type="pdf")

if uploaded_file:
    with st.spinner("Analyzing the syllabus..."):
        syllabus_text = read_pdf(uploaded_file)
        st.sidebar.success("Syllabus Loaded!")

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask me anything (e.g. Explain Ohm's Law with an example)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # The "Prompt Engineering" - Telling the AI how to behave
            context_prompt = f"""
            You are a Class 10 CBSE Science Teacher. 
            Use the following text from the NCERT textbook to answer the student's question accurately.
            If the answer is not in the text, use your general science knowledge but stay within the CBSE Class 10 syllabus.
            Provide: 
            1. A simple explanation.
            2. The formula (if any).
            3. A common exam question on this topic.
            
            Textbook Context: {syllabus_text[:5000]} # Using first 5000 chars for speed
            
            Student Question: {prompt}
            """
            
            response = model.generate_content(context_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.info("👋 Welcome! Please upload your Science NCERT PDF in the sidebar to start learning with the AI Tutor.")
    st.image("https://ncert.nic.in/textbook/pdf/jesc110.pdf", caption="Try uploading a chapter from NCERT", width=300)

# SIDEBAR INFO
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Ask the bot to generate MCQs or explain diagrams from the text!")
