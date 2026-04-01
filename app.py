import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science AI Tutor", page_icon="🧬", layout="wide")

# --- GOOGLE AI AUTO-SETUP ---
def initialize_bot():
    try:
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        
        # This part asks Google which models are available for your API key
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            st.error("Your API key doesn't have access to any models yet.")
            return None

        # Prefer 1.5-flash, then 1.5-pro, then gemini-pro
        selected_model_name = ""
        for name in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
            if name in available_models:
                selected_model_name = name
                break
        
        if not selected_model_name:
            selected_model_name = available_models[0] # Just pick the first one available
            
        return genai.GenerativeModel(selected_model_name)
            
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return None

# Load the model once
if "model" not in st.session_state:
    st.session_state.model = initialize_bot()

def clean_text(text):
    """Deep clean text to prevent API errors"""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

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
    if "syllabus_text" not in st.session_state:
        with st.spinner("Analyzing the syllabus..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Tutor is thinking..."):
                    context = st.session_state.syllabus_text[:7000] # Safe context length
                    
                    final_prompt = f"""
                    You are a CBSE Science teacher. Use this NCERT data: {context}
                    
                    Student Question: {prompt}
                    
                    Rules: Give a clear answer, a formula if applicable, and one board-exam tip.
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(final_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error("I'm having trouble with that request. Try a different topic.")
                        st.caption(f"Details: {e}")
            else:
                st.error("AI not available. Please check your API key.")

else:
    st.info("👋 Upload a Science NCERT PDF to start your session.")
