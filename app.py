import streamlit as st
import PyPDF2
import io

# --- UI CONFIG ---
st.set_page_config(page_title="CBSE Class 10 Science - Full Access", page_icon="📖", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title { font-size:40px; color: #2E4053; font-weight: bold; text-align: center; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTION TO READ PDF ---
import pypdf  # Change this from PyPDF2 to pypdf

# --- FUNCTION TO READ PDF (UPDATED) ---
def read_pdf(file):
    try:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# --- MAIN APP ---
st.markdown('<p class="main-title">🧪 CBSE Class 10 Science: Full Syllabus Bot</p>', unsafe_allow_html=True)

# SIDEBAR: SOURCE SELECTION
st.sidebar.title("🛠️ Knowledge Source")
source = st.sidebar.radio("Choose Source:", ["NCERT Digital Hub", "Upload PDF Book", "Cheat Sheets"])

if source == "Upload PDF Book":
    st.header("📂 Upload NCERT Science PDF")
    st.info("You can download the official NCERT PDF from ncert.nic.in and upload it here.")
    uploaded_file = st.file_uploader("Choose the Science Book PDF", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Bot is reading the book..."):
            book_text = read_pdf(uploaded_file)
            st.success("Book Loaded Successfully!")
            
            # Search Feature within PDF
            query = st.text_input("🔍 Ask anything from the uploaded book (e.g., 'What is Tyndall Effect?')")
            if query:
                # Basic search logic to find relevant sentences
                results = [line for line in book_text.split('.') if query.lower() in line.lower()]
                if results:
                    st.write("### 🤖 Bot's Answer (Found in PDF):")
                    for r in results[:3]: # Show top 3 results
                        st.write(f"- {r.strip()}.")
                else:
                    st.warning("Sorry, I couldn't find that specific topic in the PDF. Try different keywords.")

elif source == "NCERT Digital Hub":
    st.header("🌍 Official NCERT Resources")
    st.write("Since the full syllabus is vast, use these direct links for the 2026-27 pattern:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📘 Download Full Science Book (PDF)", "https://ncert.nic.in/textbook.php?jesc1=0-13")
        st.link_button("🧪 Chemistry Chapters", "https://ncert.nic.in/textbook.php?jesc1=1-4")
    with col2:
        st.link_button("🧬 Biology Chapters", "https://ncert.nic.in/textbook.php?jesc1=5-8")
        st.link_button("⚡ Physics Chapters", "https://ncert.nic.in/textbook.php?jesc1=9-12")

    st.divider()
    st.subheader("💡 Study Tip")
    st.write("The 2026-27 Board exams focus heavily on **Competency Based Questions**. Don't just memorize definitions; understand the 'Why' behind every experiment!")

elif source == "Cheat Sheets":
    st.header("⚡ Chapter-wise Formula & Concept Cheat Sheets")
    chapter = st.selectbox("Select Chapter", ["Chemical Reactions", "Acids, Bases & Salts", "Metals & Non-metals", "Life Processes", "Light", "Electricity"])
    
    # Example for one chapter - you can expand this
    if chapter == "Electricity":
        st.code("""
        - V = IR (Ohm's Law)
        - P = VI = I²R = V²/R
        - R = ρL/A
        - Series: Rs = R1 + R2 + R3
        - Parallel: 1/Rp = 1/R1 + 1/R2 + 1/R3
        - 1 kWh = 3.6 × 10⁶ Joules
        """, language="markdown")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ohm%27s_law_setup.svg/300px-Ohm%27s_law_setup.svg.png")

# FOOTER
st.sidebar.markdown("---")
st.sidebar.write("✅ **Bot Status:** Online")
st.sidebar.write("🎓 **Class:** 10th CBSE")
