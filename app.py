import streamlit as st

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Class 10 Science Hub 2026-27", page_icon="🎓", layout="wide")

# --- STYLING (FIXED PARAMETER) ---
st.markdown("""
    <style>
    .main-title { font-size:42px; color: #FF4B4B; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .cheat-box { background-color: #f0f2f6; padding: 20px; border-radius: 12px; border-left: 6px solid #00c0f2; margin-bottom: 15px; }
    .formula-box { background-color: #e8f5e9; padding: 20px; border-radius: 12px; border-left: 6px solid #2e7d32; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- THE MEGA DATASET (ALL 13 NCERT CHAPTERS) ---
data = {
    "🧪 Chemistry": {
        "Ch 1: Chemical Reactions": {
            "Cheat Sheet": """🌈 **Colors:** AgCl (White), CuO (Black), FeSO4 (Green). <br>⚖️ **Law:** Mass is neither created nor destroyed.""",
            "Formulas": """• Combination: A + B → AB <br>• Decomposition: AB → A + B <br>• Redox: Oxidation (Loss of e-) & Reduction (Gain of e-)""",
            "Concepts": """Types of reactions: Combination, Decomposition, Displacement, Double Displacement, Oxidation, and Reduction.""",
            "MCQs": ["1. Fe2O3 + 2Al → Al2O3 + 2Fe is? Ans: Displacement", "2. Respiration is? Ans: Exothermic"],
            "Diagrams": [{"title": "Electrolysis of Water", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Electrolysis_of_water.svg/300px-Electrolysis_of_water.svg.png"}]
        },
        "Ch 2: Acids, Bases & Salts": {
            "Cheat Sheet": """🍋 **pH < 7:** Acid (H+). <br>🧼 **pH > 7:** Base (OH-). <br>🦷 **Tooth Decay:** Starts at pH 5.5.""",
            "Formulas": """• Acid + Base → Salt + Water <br>• Bleaching Powder: CaOCl2 <br>• Baking Soda: NaHCO3 <br>• Plaster of Paris: CaSO4.1/2H2O""",
            "Concepts": """Indicators, pH scale importance, and manufacturing of Sodium Hydroxide (Chlor-alkali).""",
            "MCQs": ["1. Acid in Tomato? Ans: Oxalic Acid", "2. pH of pure water? Ans: 7"],
            "Diagrams": [{"title": "pH Scale", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PH_Scale.svg/400px-PH_Scale.svg.png"}]
        },
        "Ch 3: Metals & Non-Metals": {
            "Cheat Sheet": """🔥 **Amphoteric:** Al2O3 and ZnO. <br>💎 **Ionic Bonds:** Transfer of electrons, high melting points.""",
            "Formulas": """• Roasting: Sulphide + O2 <br>• Calcination: Carbonate + Heat""",
            "Concepts": """Reactivity series, properties of ionic compounds, and basic metallurgical processes.""",
            "MCQs": ["1. Metal that melts on palm? Ans: Gallium", "2. Non-metal that conducts? Ans: Graphite"],
            "Diagrams": [{"title": "Electrolytic Refining", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Electrolytic_refining_of_copper.png/300px-Electrolytic_refining_of_copper.png"}]
        },
        "Ch 4: Carbon & Its Compounds": {
            "Cheat Sheet": """🔗 **Catenation:** Carbon chains. <br>🧼 **Saponification:** Ester + NaOH → Soap + Alcohol.""",
            "Formulas": """• Alkanes: CnH2n+2 <br>• Alkenes: CnH2n <br>• Alkynes: CnH2n-2""",
            "Concepts": """Tetravalency, Homologous series, and nomenclature of functional groups.""",
            "MCQs": ["1. Valency of Carbon? Ans: 4", "2. Vinegar is? Ans: 5-8% Acetic Acid"],
            "Diagrams": [{"title": "Electron Dot Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Micelle_scheme-en.svg/300px-Micelle_scheme-en.svg.png"}]
        }
    },
    "🧬 Biology": {
        "Ch 5: Life Processes": {
            "Cheat Sheet": """🍎 **Nutrition:** Villi for absorption. <br>🫁 **Lungs:** Alveoli for gas exchange.""",
            "Formulas": """• Aerobic: Glucose + O2 → CO2 + H2O + 38 ATP""",
            "Concepts": """Digestive, Respiratory, Circulatory (Heart), and Excretory systems (Nephrons).""",
            "MCQs": ["1. Pumping organ? Ans: Heart", "2. Site of Bile production? Ans: Liver"],
            "Diagrams": [{"title": "Human Heart", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/300px-Diagram_of_the_human_heart_%28cropped%29.svg.png"}]
        },
        "Ch 6: Control & Coordination": {
            "Cheat Sheet": """🧠 **Brain:** Forebrain (Thinking). <br>🌿 **Auxin:** Growth at tips.""",
            "Formulas": """• Reflex Arc: Stimulus → Receptor → Spinal Cord → Effector""",
            "Concepts": """Nervous system, voluntary/involuntary actions, and hormonal coordination in plants/animals.""",
            "MCQs": ["1. Master Gland? Ans: Pituitary", "2. Controls Posture? Ans: Cerebellum"],
            "Diagrams": [{"title": "Neuron Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Blausen_0657_MultipolarNeuron.png/300px-Blausen_0657_MultipolarNeuron.png"}]
        },
        "Ch 7: How do Organisms Reproduce?": {
            "Cheat Sheet": """🍓 **Budding:** Yeast/Hydra. <br>🌸 **Carpel:** Stigma, Style, Ovary.""",
            "Formulas": """• Asexual (Clones) vs Sexual (Variations)""",
            "Concepts": """Methods of reproduction, male/female human systems, and reproductive health.""",
            "MCQs": ["1. Fission in Leishmania? Ans: Binary", "2. Part of seed? Ans: Cotyledon"],
            "Diagrams": [{"title": "Flower Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Mature_flower_diagram.svg/300px-Mature_flower_diagram.svg.png"}]
        },
        "Ch 8: Heredity": {
            "Cheat Sheet": """🧬 **Gene:** Unit of heredity. <br>👨‍🔬 **Mendel:** Used Garden Pea (Pisum sativum).""",
            "Formulas": """• F2 Ratio: 3:1 (Monohybrid) / 9:3:3:1 (Dihybrid)""",
            "Concepts": """Rules for inheritance of traits and sex determination in humans.""",
            "MCQs": ["1. Dominant trait in pea? Ans: Round/Tall", "2. Human chromosomes? Ans: 23 pairs"],
            "Diagrams": [{"title": "Sex Determination", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Human_chromosomes_XX_and_XY.png/300px-Human_chromosomes_XX_and_XY.png"}]
        }
    },
    "⚡ Physics": {
        "Ch 9: Light: Reflection & Refraction": {
            "Cheat Sheet": """🪞 **Mirror:** u is always negative. <br>🔍 **Lens:** Converging is Convex.""",
            "Formulas": """• Mirror: 1/v + 1/u = 1/f <br>• Lens: 1/v - 1/u = 1/f <br>• Power: P = 1/f(m)""",
            "Concepts": """Laws of reflection/refraction, image formation by spherical mirrors and lenses.""",
            "MCQs": ["1. Mirror for shaving? Ans: Concave", "2. Refractive index of air? Ans: 1.0003"],
            "Diagrams": [{"title": "Refraction through Glass Slab", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Refraction_photo.png/300px-Refraction_photo.png"}]
        },
        "Ch 10: Human Eye": {
            "Cheat Sheet": """👓 **Myopia:** Fixed by Concave. <br>🌈 **Atmospheric Refraction:** Twinkling stars.""",
            "Formulas": """• Dispersion: White light splitting into VIBGYOR.""",
            "Concepts": """Accommodation, defects of vision, and natural optical phenomena.""",
            "MCQs": ["1. Image formed on? Ans: Retina", "2. Danger signal color? Ans: Red (Scatters least)"],
            "Diagrams": [{"title": "Human Eye", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Schematic_diagram_of_the_human_eye_en.svg/400px-Schematic_diagram_of_the_human_eye_en.svg.png"}]
        },
        "Ch 11: Electricity": {
            "Cheat Sheet": """💡 **Ohm's Law:** V=IR. <br>🌡️ **Resistance:** Proportional to Length, Inverse to Area.""",
            "Formulas": """• P = VI <br>• H = I²Rt <br>• Series: R1+R2... <br>• Parallel: 1/R1 + 1/R2...""",
            "Concepts": """Current, Potential difference, Resistance, and heating effects.""",
            "MCQs": ["1. SI unit of Resistivity? Ans: Ωm", "2. Device to measure current? Ans: Ammeter"],
            "Diagrams": [{"title": "Circuit Diagram", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ohm%27s_law_setup.svg/300px-Ohm%27s_law_setup.svg.png"}]
        },
        "Ch 12: Magnetic Effects": {
            "Cheat Sheet": """🧲 **Lines:** Closed curves. <br>🌀 **Solenoid:** Magnetic field inside is uniform.""",
            "Formulas": """• Fleming's Left Hand Rule: Force, Field, Current.""",
            "Concepts": """Magnetic fields, Right-hand thumb rule, Solenoid, and Domestic electric circuits.""",
            "MCQs": ["1. Magnetic field unit? Ans: Tesla", "2. Direct Current freq? Ans: 0 Hz"],
            "Diagrams": [{"title": "Magnetic Field lines", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/VFPt_cylindrical_magnet_thumb.svg/300px-VFPt_cylindrical_magnet_thumb.svg.png"}]
        }
    },
    "🌍 Environment": {
        "Ch 13: Our Environment": {
            "Cheat Sheet": """♻️ **10% Law:** Energy decrease at each level. <br>☀️ **Ozone (O3):** Protects from UV rays.""",
            "Formulas": """• Producers → Herbivores → Carnivores""",
            "Concepts": """Eco-system, food chains, ozone depletion, and waste disposal.""",
            "MCQs": ["1. First trophic level? Ans: Producers", "2. Which are decomposers? Ans: Bacteria/Fungi"],
            "Diagrams": [{"title": "Trophic Levels", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Energy_pyramid.svg/300px-Energy_pyramid.svg.png"}]
        }
    }
}

# --- RENDERING LOGIC ---
st.markdown('<p class="main-title">🚀 CBSE Class 10 Science Bot (2026-27)</p>', unsafe_allow_html=True)

# SIDEBAR NAV
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/583/583325.png", width=80)
st.sidebar.header("Study Navigator")
subject = st.sidebar.selectbox("📂 Select Subject", list(data.keys()))
chapter = st.sidebar.selectbox("📖 Select Chapter", list(data[subject].keys()))
mode = st.sidebar.radio("🎯 Learning Goal", ["⚡ Cheat Sheet & Formulas", "📘 Detailed Concepts", "📝 MCQs & Questions", "🖼️ Diagrams"])

# CONTENT DISPLAY
content = data[subject][chapter]

if mode == "⚡ Cheat Sheet & Formulas":
    st.header(f"⚡ Revision: {chapter}")
    st.markdown(f'<div class="cheat-box"><h3>📝 Cheat Sheet</h3>{content["Cheat Sheet"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="formula-box"><h3>🔢 Formulas/Key Laws</h3>{content["Formulas"]}</div>', unsafe_allow_html=True)

elif mode == "📘 Detailed Concepts":
    st.header(f"📘 Full Concept: {chapter}")
    st.info(content["Concepts"])
    st.markdown("---")
    st.success("📚 Note: Stick to NCERT keywords for maximum marks in Boards!")

elif mode == "📝 MCQs & Questions":
    st.header(f"✍️ Practice: {chapter}")
    for q in content["MCQs"]:
        with st.expander("Click to View Question & Answer"):
            st.write(q)

elif mode == "🖼️ Diagrams":
    st.header(f"🎨 Visuals: {chapter}")
    for d in content["Diagrams"]:
        st.subheader(d["title"])
        st.image(d["url"], use_container_width=True)

# SIDEBAR FOOTER
st.sidebar.markdown("---")
st.sidebar.write("✅ **Syllabus:** CBSE 2026-27")
st.sidebar.write("👨‍🏫 **Target:** Class 10 Board Exams")
st.sidebar.caption("Designed for Academic Excellence 🏆")
