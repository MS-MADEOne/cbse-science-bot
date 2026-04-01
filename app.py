import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests
import time

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Hub Pro", page_icon="🧪", layout="wide")

# --- 2. STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .main-title { font-size:42px; background: -webkit-linear-gradient(#1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; margin-bottom: 20px; }
    .info-card { padding: 20px; border-radius: 18px; color: white; margin-bottom: 12px; min-height: 140px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .blue-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
    .green-card { background: linear-gradient(135deg, #065F46 0%, #10B981 100%); }
    .orange-card { background: linear-gradient(135deg, #9A3412 0%, #F97316 100%); }
    .purple-card { background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%); }
    .flashcard { background: #ffffff; border-radius: 15px; padding: 15px; border-left: 8px solid #3B82F6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; color: #333; border: 1px solid #eee; }
    .formula-tag { display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 50px; font-weight: 700; margin: 4px; font-size: 14px; border: 1px solid #BFDBFE; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI ENGINES ---
@st.cache_resource
def init_ai_engine():
    try:
        if "GEMINI_KEY" not in st.secrets: return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

ai_model = init_ai_engine()

@st.cache_data
def get_clean_text(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            text = " ".join([page.extract_text() for page in pdf.pages])
            return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()
    except: return ""

def get_wiki_img(q):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={q}"
        return requests.get(url).json()['query']['pages'][0]['original']['source']
    except: return None

# --- 4. ROBUST KEYWORD PARSER ---
def parse_study_kit(text):
    sections = {"bento": [], "formulas": [], "tips": []}
    lines = text.split('\n')
    for line in lines:
        clean = line.strip().replace('- ', '').replace('* ', '')
        if 'CONCEPT:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'APP:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'EXP:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FOCUS:' in clean.upper(): sections["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FORMULA:' in clean.upper(): sections["formulas"].append(clean.split(':', 1)[-1].strip())
        elif 'TIP:' in clean.upper(): sections["tips"].append(clean.split(':', 1)[-1].strip())
    while len(sections["bento"]) < 4: sections["bento"].append("Refer to NCERT textbook.")
    return sections

# --- 5. MAIN APP INTERFACE ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR): os.makedirs(SYLLABUS_DIR)
pdf_files = sorted([f for f in os.listdir(SYLLABUS_DIR) if f.endswith(".pdf")])

# Initialize session state
if "msgs" not in st.session_state: st.session_state.msgs = []

if pdf_files:
    chapter = st.sidebar.selectbox("📂 Select Chapter", pdf_files)
    raw_text = get_clean_text(os.path.join(SYLLABUS_DIR, chapter))

    # CACHED AI CALL FOR STUDY KIT
    @st.cache_data(show_spinner=False)
    def get_ai_kit(chap_name, text_content):
        prompt = f"Analyze: {text_content[:6000]}. Provide labels: CONCEPT:, APP:, EXP:, FOCUS:, FORMULA: (list 4), TIP: (list 4)."
        try:
            response = ai_model.generate_content(prompt)
            return parse_study_kit(response.text)
        except Exception as e:
            if "429" in str(e): return "QUOTA_ERROR"
            return None

    # Logic to handle the "Generate" Button
    if st.sidebar.button("✨ Generate Visual Study Kit"):
        kit_result = get_ai_kit(chapter, raw_text)
        if kit_result == "QUOTA_ERROR":
            st.sidebar.error("🚨 AI is resting! Please wait 60 seconds and try again.")
        elif kit_result:
            st.session_state.kit_data = kit_result
            st.sidebar.success("✅ Study Kit Ready!")
        else:
            st.sidebar.error("Something went wrong. Check API Key.")

else:
    st.sidebar.warning("Upload PDFs to 'ncert_syllabus' folder on GitHub!")
    st.sto
