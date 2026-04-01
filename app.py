import streamlit as st
import pypdf
import google.generativeai as genai
import re
import requests

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Science Visual Tutor", page_icon="🧪", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #D35400; font-weight: bold; text-align: center; }
    .video-box { border: 2px solid #E74C3C; border-radius: 10px; padding: 10px; margin-top: 10px; }
    .image-box { border: 2px solid #27AE60; border-radius: 10px; padding: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS FOR VISUALS ---

def get_wikimedia_image(query):
    """Fetches a scientific diagram from Wikimedia Commons"""
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={query}"
        response = requests.get(url).json()
        page = response['query']['pages'][0]
        return page['original']['source'] if 'original' in page else None
    except:
        return None

def get_youtube_embed(query):
    """Creates a YouTube search link for the topic"""
    search_url = f"https://www.youtube.com/results?search_query=cbse+class+10+science+{query.replace(' ', '+')}"
    return search_url

# --- GOOGLE AI AUTO-SETUP ---
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
st.markdown("<h1 class='main-title'>🧪 CBSE Class 10 Visual AI Tutor</h1>", unsafe_allow_html=True)

st.sidebar.title("📚 Study Material")
uploaded_file = st.sidebar.file_uploader("Upload NCERT Science PDF", type="pdf")

if uploaded_file:
    if "syllabus_text" not in st.session_state:
        with st.spinner("Analyzing Textbook..."):
            st.session_state.syllabus_text = read_pdf(uploaded_file)
            st.sidebar.success("Syllabus Loaded!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question (e.g. Explain the Human Eye)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.model:
                with st.spinner("Tutor is preparing answer with visuals..."):
                    context = st.session_state.syllabus_text[:7000]
                    
                    # PROMPT MODIFIED TO ASK FOR A VISUAL KEYWORD
                    final_prompt = f"""
                    Context: {context}
                    Question: {prompt}
                    
                    Instructions: 
                    1. Answer as a CBSE Science teacher.
                    2. At the very end of your answer, write: 'VISUAL_KEYWORD: [Single most relevant scientific term for a diagram]'.
                    """
                    
                    try:
                        response = st.session_state.model.generate_content(final_prompt)
                        full_text = response.text
                        
                        # Extract Keyword for Visuals
                        visual_keyword = ""
                        if "VISUAL_KEYWORD:" in full_text:
                            parts = full_text.split("VISUAL_KEYWORD:")
                            full_text = parts[0] # Clean text answer
                            visual_keyword = parts[1].strip().replace('[', '').replace(']', '').split('\n')[0]

                        # Display Answer
                        st.markdown(full_text)
                        
                        # Display Visuals
                        if visual_keyword:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                img_url = get_wikimedia_image(visual_keyword)
                                if img_url:
                                    st.markdown("<div class='image-box'><b>🖼️ Reference Diagram:</b></div>", unsafe_allow_html=True)
                                    st.image(img_url, caption=f"Diagram of {visual_keyword}")
                                else:
                                    st.info("No diagram found, but you can check the textbook for visuals!")

                            with col2:
                                vid_link = get_youtube_embed(visual_keyword)
                                st.markdown("<div class='video-box'><b>📺 Video Explanation:</b></div>", unsafe_allow_html=True)
                                st.write(f"Watch live experiment/animation:")
                                st.link_button(f"▶️ Watch {visual_keyword} Video", vid_link)

                        st.session_state.messages.append({"role": "assistant", "content": full_text})
                    except Exception as e:
                        st.error("I hit a snag. Try asking a shorter question.")
            else:
                st.error("AI setup incomplete.")

else:
    st.info("👋 Upload a Science NCERT PDF to see answers with diagrams and videos!")
