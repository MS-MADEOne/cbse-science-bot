import streamlit as st

# --- DATASET (Sample - You can expand this) ---
data = {
    "Physics": {
        "Light: Reflection & Refraction": {
            "Concepts": "Reflection: Bouncing back of light. Refraction: Bending of light when entering different media.",
            "MCQs": ["1. Focal length of plane mirror is? \nAns: Infinity", "2. Unit of Power? \nAns: Dioptre"],
            "Short Answers": ["Q: Define 1 Dioptre. \nA: Power of a lens whose focal length is 1 meter."],
            "Diagrams": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Reflection_angles.svg/300px-Reflection_angles.svg.png"
        }
    },
    "Chemistry": {
        "Chemical Reactions": {
            "Concepts": "Combination, Decomposition, Displacement, Redox reactions.",
            "MCQs": ["1. Burning of Magnesium is? \nAns: Oxidation"],
            "Short Answers": ["Q: Why is respiration considered exothermic? \nA: Because energy is released during the process."],
            "Diagrams": "https://example.com/chemical_setup_diagram.jpg"
        }
    }
}

# --- UI CONFIG ---
st.set_page_config(page_title="Class 10 CBSE Science Bot", page_icon="🧪")
st.title("🧪 CBSE Class 10 Science Assistant")
st.sidebar.header("Select Chapter")

# --- SELECTION LOGIC ---
subject = st.sidebar.selectbox("Choose Subject", list(data.keys()))
chapter = st.sidebar.selectbox("Choose Chapter", list(data[subject].keys()))
category = st.sidebar.radio("What do you need?", ["Concepts", "MCQs", "Short Answers", "Diagrams"])

# --- DISPLAY CONTENT ---
st.header(f"{chapter} - {category}")

content = data[subject][chapter][category]

if category == "Diagrams":
    st.image(content, caption=f"Diagram for {chapter}")
elif isinstance(content, list):
    for item in content:
        st.write(item)
        st.divider()
else:
    st.write(content)

# --- CHATBOT FEATURE ---
st.sidebar.divider()
st.sidebar.subheader("Quick Search")
user_query = st.sidebar.text_input("Ask a quick question:")
if user_query:
    st.info(f"Searching for '{user_query}' in CBSE Syllabus...")
    # Here you can add logic to search the 'data' dictionary
    st.write("Feature coming soon: AI-based quick search!")

st.caption("Developed for Class 10 CBSE Students")
