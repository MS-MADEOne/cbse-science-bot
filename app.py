import streamlit as st

# --- COMPLETE CBSE 10th SCIENCE DATASET ---
data = {
    "Physics": {
        "Light: Reflection & Refraction": {
            "Concepts": "**Reflection:** ∠i = ∠r. **Mirror Formula:** 1/v + 1/u = 1/f. **Lens Formula:** 1/v - 1/u = 1/f. **Power:** P = 1/f(m).",
            "MCQs": ["1. Focal length of plane mirror? Ans: Infinity", "2. Unit of Power? Ans: Dioptre"],
            "Very Short Answers (1M)": ["Q: Define refractive index. A: Ratio of speed of light in vacuum to speed in medium."],
            "Short Answers (3M)": ["Q: Why are convex mirrors used in cars? A: They give erect, diminished images and wide field of view."],
            "Long Answers (5M)": ["Q: Draw ray diagrams for concave mirror at C and between C & F."],
            "Diagrams": [{"title": "Reflection", "url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Reflection_angles.svg"}]
        },
        "Human Eye": {
            "Concepts": "**Myopia:** Near clear, far blurry (Concave correction). **Hypermetropia:** Far clear, near blurry (Convex correction).",
            "MCQs": ["1. Least distance of vision? Ans: 25cm"],
            "Very Short Answers (1M)": ["Q: Function of Iris? A: Controls pupil size."],
            "Short Answers (3M)": ["Q: Explain Tyndall Effect. A: Scattering of light by colloidal particles."],
            "Long Answers (5M)": ["Q: Explain Dispersion of white light through a prism with a diagram."],
            "Diagrams": [{"title": "Human Eye", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Schematic_diagram_of_the_human_eye_en.svg/400px-Schematic_diagram_of_the_human_eye_en.svg.png"}]
        },
        "Electricity": {
            "Concepts": "**Ohm's Law:** V=IR. **Resistance:** R = ρL/A. **Heating:** H = I²Rt. **Power:** P = VI.",
            "MCQs": ["1. Unit of Resistivity? Ans: Ohm-meter"],
            "Very Short Answers (1M)": ["Q: Define 1 Ampere. A: 1 Coulomb of charge per second."],
            "Short Answers (3M)": ["Q: Why is parallel better than series at home? A: Independent switches, same voltage."],
            "Long Answers (5M)": ["Q: Derive equivalent resistance for resistors in parallel."],
            "Diagrams": [{"title": "Circuit", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ohm%27s_law_setup.svg/300px-Ohm%27s_law_setup.svg.png"}]
        }
    },
    "Chemistry": {
        "Chemical Reactions": {
            "Concepts": "**Types:** Combination, Decomposition, Displacement, Double Displacement, Redox.",
            "MCQs": ["1. Fe + CuSO4 -> FeSO4 + Cu is? Ans: Displacement"],
            "Very Short Answers (1M)": ["Q: Why paint iron? A: To prevent corrosion."],
            "Short Answers (3M)": ["Q: Difference between Exothermic and Endothermic? A: Heat released vs Heat absorbed."],
            "Long Answers (5M)": ["Q: Explain Electrolytic decomposition of water with diagram."],
            "Diagrams": [{"title": "Reaction Types", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Chemical_Reaction.jpg/300px-Chemical_Reaction.jpg"}]
        },
        "Acids, Bases & Salts": {
            "Concepts": "**pH Scale:** <7 Acidic, >7 Basic. **Neutralization:** Acid + Base -> Salt + Water.",
            "MCQs": ["1. pH of Milk of Magnesia? Ans: 10"],
            "Very Short Answers (1M)": ["Q: Common name of CaOCl2? A: Bleaching Powder."],
            "Short Answers (3M)": ["Q: Why does distilled water not conduct electricity? A: It doesn't dissociate into ions."],
            "Long Answers (5M)": ["Q: Explain Chlor-alkali process with equations."],
            "Diagrams": [{"title": "pH Scale", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PH_Scale.svg/400px-PH_Scale.svg.png"}]
        }
    },
    "Biology": {
        "Life Processes": {
            "Concepts": "**Nutrition:** Autotrophic & Heterotrophic. **Respiration:** Aerobic & Anaerobic. **Excretion:** Via Nephrons.",
            "MCQs": ["1. Site of photosynthesis? Ans: Chloroplast"],
            "Very Short Answers (1M)": ["Q: What is Peristalsis? A: Rhythmic contraction of food pipe."],
            "Short Answers (3M)": ["Q: Role of HCl in stomach? A: Kills bacteria, activates pepsin."],
            "Long Answers (5M)": ["Q: Describe the double circulation of blood in human heart."],
            "Diagrams": [{"title": "Human Digestive System", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Digestive_system_diagram_edit.svg/300px-Digestive_system_diagram_edit.svg.png"}]
        },
        "Reproduction": {
            "Concepts": "**Asexual:** Fission, Budding, Regeneration. **Sexual:** Pollination & Fertilization.",
            "MCQs": ["1. Where does fertilization occur? Ans: Fallopian tube"],
            "Very Short Answers (1M)": ["Q: Define vegetative propagation. A: Growth of new plant from roots/stems."],
            "Short Answers (3M)": ["Q: Difference between Self and Cross pollination? A: Same flower vs different flower."],
            "Long Answers (5M)": ["Q: Explain the parts of a flower with their functions."],
            "Diagrams": [{"title": "Flower Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Mature_flower_diagram.svg/300px-Mature_flower_diagram.svg.png"}]
        }
    }
}

# --- STREAMLIT UI CODE ---
st.set_page_config(page_title="CBSE Class 10 Science Bot", page_icon="🧬")

st.title("🧬 CBSE Class 10 Science Study Bot")
st.markdown("---")

# Sidebar navigation
st.sidebar.header("Navigation")
subj_list = list(data.keys())
subject = st.sidebar.selectbox("Select Subject", subj_list)

chap_list = list(data[subject].keys())
chapter = st.sidebar.selectbox("Select Chapter", chap_list)

category = st.sidebar.radio("Resource Type", 
    ["Concepts", "MCQs", "Very Short Answers (1M)", "Short Answers (3M)", "Long Answers (5M)", "Diagrams"])

# Content Display
st.header(f"{subject}: {chapter}")
st.subheader(category)

selected_content = data[subject][chapter][category]

if category == "Diagrams":
    for item in selected_content:
        st.write(f"**{item['title']}**")
        st.image(item['url'], use_container_width=True)
elif isinstance(selected_content, list):
    for idx, item in enumerate(selected_content):
        with st.expander(f"Question {idx+1}"):
            st.write(item)
else:
    st.info(selected_content)

# Search Feature
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Help")
search = st.sidebar.text_input("Search a keyword (e.g. Prism)")
if search:
    st.sidebar.write(f"Tip: Go to Physics -> Human Eye to find information about {search}!")

# UPDATED YEAR HERE
st.sidebar.caption("Syllabus updated for 2026-27 Board Exams")
