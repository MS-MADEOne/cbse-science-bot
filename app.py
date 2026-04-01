import streamlit as st
import pypdf
import google.generativeai as genai
import re

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science AI Tutor", page_icon="🧬", layout="wide")

# --- GOOGLE AI SETUP ---
def get_model():
    try:
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        
        # We try 1.5-flash first as it's better for documents
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Test if model exists by sending a tiny probe
            model.generate_content("test") 
            return model
        except Exception:
            # Fallback to the most stable legacy model if 1.5-flash fails
            return genai.GenerativeModel('gemini-pro')
            
    except Exception as e:
        st.error("API Key Error. Check Streamlit Secrets.")
        return None

model = get_model()

def clean_text(text):
    """Clean PDF text to remove non-compatible characters"""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # Remove non-ASCII
    text = text.replace('"', "'") # Escape quotes
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
    if "syllabus_text" not in st.session_state:
        with st.spinner("Analyzing the syllabus..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question (e.g. Explain photosynthesis)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if model:
                with st.spinner("Searching the textbook..."):
                    # Use a safer, smaller context window
                    context = st.session_state.syllabus_text[:5000]
                    
                    final_prompt = f"""
                    Context from NCERT: {context}
                    
                    Question: {prompt}
                    
                    Instruction: You are a CBSE Science teacher. Answer clearly using the context provided. 
                    If not in context, answer from CBSE Class 10 knowledge.
                    """
                    
                    try:
                        response = model.generate_content(final_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error("Model Error. Try a simpler question.")
                        st.caption(f"Error: {e}")
            else:
                st.error("AI Model not initialized.")

else:
    st.info("👋 Welcome! Please upload a Science NCERT PDF (Chapter or Full Book) to begin.")
