import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science AI Tutor", page_icon="🧬", layout="wide")

# --- GOOGLE AI SETUP ---
try:
    # Fetch API Key from Streamlit Secrets
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    # Using 'gemini-1.5-flash' - it is faster and better at handling text context
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Missing GEMINI_KEY in Secrets or API Error. Check your Streamlit Dashboard.")

def clean_text(text):
    """Removes special characters that break the AI request"""
    # Remove non-printable characters and keep basic punctuation
    text = re.sub(r'[^\x20-\x7E]+', ' ', text)
    return text

def read_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return clean_text(text)

# --- APP INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🤖 CBSE Science AI Tutor</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Study Material")
uploaded_file = st.sidebar.file_uploader("Upload NCERT Science PDF", type="pdf")

if uploaded_file:
    # Using session_state to save text so we don't re-read the PDF every time
    if "syllabus_text" not in st.session_state:
        with st.spinner("Analyzing the syllabus..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Loaded!")

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask a question from the syllabus..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # We only send a part of the text (e.g., first 8000 chars) to prevent 'Token Limit' errors
                context = st.session_state.syllabus_text[:8000] 
                
                final_prompt = f"""
                You are a professional CBSE Class 10 Science Teacher. 
                Use this textbook data: {context}
                
                Answer this question: {prompt}
                
                Rules:
                1. If it is a law/definition, state it clearly.
                2. Use bullet points for steps/processes.
                3. Suggest one 'Important for Boards' question related to this.
                """
                
                try:
                    response = model.generate_content(final_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("The AI had trouble processing this. Try asking a shorter question.")
                    st.write(f"Error Details: {e}")

else:
    st.info("👋 Welcome! Upload your NCERT Science PDF (Chapters or Full Book) to start.")
    st.image("https://ncert.nic.in/textbook/pdf/jesc101.pdf", caption="Example: Chapter 1 - Chemical Reactions", width=250)
