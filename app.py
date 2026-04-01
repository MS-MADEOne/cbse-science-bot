import streamlit as st
import pypdf
import google.generativeai as genai
import re
import os
import requests

# --- 1. UI CONFIG ---
st.set_page_config(page_title="CBSE Science Pro 2027", page_icon="🧪", layout="wide")

# --- 2. STYLING (KEEPING IT BEAUTIFUL) ---
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

# --- 3. ROBUST AI INITIALIZATION ---
def get_ai_model():
    try:
        if "GEMINI_KEY" not in st.secrets:
            st.error("🔑 API Key not found! Add 'GEMINI_KEY' in Streamlit Secrets.")
            return None
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # We use gemini-1.5-flash as it's the most reliable for Free Tier
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

# Load the model into session state so it persists
if "model_engine" not in st.session_state:
    st.session_state.model_engine = get_ai_model()

# --- 4. DATA PROCESSING ---
@st.cache_data
def load_text_from_pdf(path):
    try:
        with open(path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            return " ".join([p.extract_text() for p in pdf.pages])
    except: return ""

def parse_kit_output(text):
    """Parses AI output by looking for specific labels"""
    res = {"bento": [], "formulas": [], "tips": []}
    lines = text.split('\n')
    for line in lines:
        clean = line.strip().replace('*', '').replace('-', '')
        if 'CONCEPT:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'APP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'EXP:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FOCUS:' in clean.upper(): res["bento"].append(clean.split(':', 1)[-1].strip())
        elif 'FORMULA:' in clean.upper(): res["formulas"].append(clean.split(':', 1)[-1].strip())
        elif 'TIP:' in clean.upper(): res["tips"].append(clean.split(':', 1)[-1].strip())
    
    # Fill defaults if AI skipped something
    while len(res["bento"]) < 4: res["bento"].append("Refer to NCERT textbook.")
    return res

# --- 5. MAIN APP ---
st.markdown("<h1 class='main-title'>🎓 CBSE Class 10 Science Pro</h1>", unsafe_allow_html=True)

SYLLABUS_DIR = "ncert_syllabus"
if not os.path.exists(SYLLABUS_DIR):
    st.info("Please create a folder 'ncert_syllabus
