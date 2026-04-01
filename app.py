import streamlit as st

# --- UI CONFIG ---
st.set_page_config(page_title="Class 10 Science - Full Syllabus Hub", page_icon="📚", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-title { font-size:45px; color: #E74C3C; font-weight: bold; text-align: center; }
    .chap-header { color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; }
    .cheat-box { background-color: #FBFCFC; padding: 20px; border-radius: 10px; border-left: 6px solid #F1C40F; margin-bottom: 15px; box-shadow: 2px 2px 5px #eee; }
    .formula-box { background-color: #F4F9F4; padding: 20px; border-radius: 10px; border-left: 6px solid #27AE60; margin-bottom: 15px; }
    .concept-card { background-color: #EBF5FB; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #2980B9; }
    </style>
    """, unsafe_allow_html=True)

# --- THE ENTIRE SYLLABUS DATASET ---
syllabus_data = {
    "🧪 Chemistry": {
        "Ch 1: Chemical Reactions": {
            "Cheat Sheet": """🔹 **Balanced Equation:** Number of atoms on LHS = RHS. <br>🔹 **Exothermic:** Heat released (Respiration). <br>🔹 **Endothermic:** Heat absorbed (Photosynthesis). <br>🔹 **Corrosion:** Oxidation of metals (Rusting of iron). <br>🔹 **Rancidity:** Oxidation of fats/oils in food.""",
            "Detailed Concepts": [
                "**1. Combination:** A + B → AB (e.g., Burning Coal)",
                "**2. Decomposition:** AB → A + B (Thermal, Electrolytic, Photolytic)",
                "**3. Displacement:** More reactive metal displaces less reactive one.",
                "**4. Double Displacement:** Exchange of ions between reactants.",
                "**5. Redox:** Oxidation (Loss of H, Gain of O) and Reduction (Gain of H, Loss of O)."
            ],
            "Formulas": "2H2 + O2 → 2H2O | CaCO3 → CaO + CO2 | Fe + CuSO4 → FeSO4 + Cu",
            "MCQs": ["Q1: Reaction of MgO with water? Ans: Basic", "Q2: Gas evolved with Zinc and Acid? Ans: Hydrogen"],
            "Diagrams": [{"title": "Electrolysis of Water", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Electrolysis_of_water.svg/300px-Electrolysis_of_water.svg.png"}]
        },
        "Ch 2: Acids, Bases & Salts": {
            "Cheat Sheet": """🔹 **Litmus:** Acid(B→R), Base(R→B). <br>🔹 **Strong Acid:** HCl, H2SO4. <br>🔹 **Strong Base:** NaOH, KOH. <br>🔹 **pH 7:** Neutral. <br>🔹 **Antacids:** Milk of Magnesia.""",
            "Detailed Concepts": [
                "**Acids:** Sour taste, H+ ions, conduct electricity in water.",
                "**Bases:** Bitter taste, soapy feel, OH- ions.",
                "**pH Scale:** Measures H+ concentration. 0-6 Acidic, 8-14 Basic.",
                "**Common Salt (NaCl):** Raw material for Bleaching powder, Baking soda, Washing soda.",
                "**Water of Crystallization:** Fixed no. of water molecules in formula (e.g., Gypsum)."
            ],
            "Formulas": "• pH = -log[H+] <br>• CaOCl2 (Bleaching) <br>• NaHCO3 (Baking Soda) <br>• Na2CO3.10H2O (Washing Soda) <br>• CaSO4.1/2H2O (P.O.P)",
            "MCQs": ["Q1: Acid in curd? Ans: Lactic", "Q2: Metal + Acid → ? Ans: Salt + Hydrogen"],
            "Diagrams": [{"title": "pH Scale", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PH_Scale.svg/400px-PH_Scale.svg.png"}]
        },
        "Ch 3: Metals & Non-Metals": {
            "Cheat Sheet": """🔹 **Lustrous:** Metals shine. <br>🔹 **Malleable:** Beaten into sheets. <br>🔹 **Ductile:** Drawn into wires. <br>🔹 **Amphoteric:** Oxides like Al2O3, ZnO.""",
            "Detailed Concepts": [
                "**Metals:** Electropositive, form basic oxides.",
                "**Non-Metals:** Electronegative, form acidic oxides.",
                "**Reactivity Series:** K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Hg > Ag > Au.",
                "**Ionic Compounds:** Strong force of attraction, high Melting Point.",
                "**Metallurgy:** Extraction (Roasting vs Calcination) and Refining."
            ],
            "Formulas": "• Anode: Impure metal | Cathode: Pure metal <br>• Brass: Cu + Zn | Bronze: Cu + Sn",
            "MCQs": ["Q1: Liquid non-metal? Ans: Bromine", "Q2: Amphoteric oxide? Ans: Al2O3"],
            "Diagrams": [{"title": "Extraction of Metals", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Electrolytic_refining_of_copper.png/300px-Electrolytic_refining_of_copper.png"}]
        },
        "Ch 4: Carbon & Its Compounds": {
            "Cheat Sheet": """🔹 **Tetravalency:** C forms 4 bonds. <br>🔹 **Catenation:** C chains. <br>🔹 **Hydrocarbons:** Saturated(Single) & Unsaturated(Double/Triple).""",
            "Detailed Concepts": [
                "**Covalent Bond:** Sharing of electrons.",
                "**Allotropes:** Diamond (Hard), Graphite (Conductor), Buckminsterfullerene.",
                "**Homologous Series:** Same functional group, CH2 difference.",
                "**Functional Groups:** Alcohol (-OH), Aldehyde (-CHO), Ketone (>C=O), Carboxylic Acid (-COOH).",
                "**Soap & Detergents:** Micelle formation and cleansing action."
            ],
            "Formulas": "• Alkanes: CnH2n+2 <br>• Alkenes: CnH2n <br>• Alkynes: CnH2n-2 <br>• Ethanol: C2H5OH",
            "MCQs": ["Q1: Simplest Alkane? Ans: Methane", "Q2: Functional group in Vinegar? Ans: Carboxylic Acid"],
            "Diagrams": [{"title": "Micelle Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Micelle_scheme-en.svg/300px-Micelle_scheme-en.svg.png"}]
        }
    },
    "🧬 Biology": {
        "Ch 5: Life Processes": {
            "Cheat Sheet": """🔹 **Autotrophic:** Plants (Photosynthesis). <br>🔹 **Bile:** Liver (Emulsification). <br>🔹 **Villi:** Small Intestine (Absorption). <br>🔹 **Nephron:** Unit of Kidney.""",
            "Detailed Concepts": [
                "**Nutrition:** Breakdown of food. Salivary amylase breaks starch.",
                "**Respiration:** Breakdown of Glucose. Aerobic (38 ATP) vs Anaerobic (2 ATP).",
                "**Transportation:** Heart (Double circulation). Xylem (Water) & Phloem (Food) in plants.",
                "**Excretion:** Removal of nitrogenous waste. Dialysis is artificial kidney."
            ],
            "Formulas": "6CO2 + 6H2O + Sunlight → C6H12O6 + 6O2",
            "MCQs": ["Q1: Pumping organ? Ans: Heart", "Q2: Site of gas exchange? Ans: Alveoli"],
            "Diagrams": [{"title": "Human Heart", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/300px-Diagram_of_the_human_heart_%28cropped%29.svg.png"}]
        },
        "Ch 6: Control & Coordination": {
            "Cheat Sheet": """🔹 **Neuron:** Nervous unit. <br>🔹 **Synapse:** Gap between neurons. <br>🔹 **Reflex Arc:** Sudden response. <br>🔹 **Phytohormones:** Plant hormones (Auxin, Cytokinin).""",
            "Detailed Concepts": [
                "**Human Brain:** Forebrain (Thinking), Midbrain, Hindbrain (Medulla, Cerebellum).",
                "**Hormones:** Insulin (Blood sugar), Adrenaline (Fight/Flight), Thyroxine (Metabolism).",
                "**Plant Movements:** Phototropism (Light), Geotropism (Gravity), Hydrotropism (Water)."
            ],
            "Formulas": "Stimulus → Receptor → Sensory Neuron → Spinal Cord → Motor Neuron → Effector",
            "MCQs": ["Q1: Part of brain for balance? Ans: Cerebellum", "2. Master gland? Ans: Pituitary"],
            "Diagrams": [{"title": "Human Brain", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Skull_and_brain_normal_human.svg/300px-Skull_and_brain_normal_human.svg.png"}]
        },
        "Ch 7: Reproduction": {
            "Cheat Sheet": """🔹 **Asexual:** Clone (Fission, Budding). <br>🔹 **DNA Copying:** Basic event of reproduction. <br>🔹 **Flower:** Stamen (M), Carpel (F). <br>🔹 **IUCD:** Copper-T.""",
            "Detailed Concepts": [
                "**Asexual:** Amoeba (Binary fission), Hydra (Budding), Rose (Vegetative).",
                "**Sexual:** Fusion of male & female gametes. Variation is high.",
                "**Human Systems:** Testes (Sperm/Testosterone), Ovaries (Egg/Estrogen).",
                "**Health:** STDs (HIV-AIDS, Gonorrhoea) and Birth Control."
            ],
            "Formulas": "Pollination (Self/Cross) → Fertilization → Zygote → Embryo",
            "MCQs": ["Q1: Site of fertilization? Ans: Fallopian Tube", "Q2: Part of seed? Ans: Cotyledon"],
            "Diagrams": [{"title": "Flower Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Mature_flower_diagram.svg/300px-Mature_flower_diagram.svg.png"}]
        }
    },
    "⚡ Physics": {
        "Ch 9: Light": {
            "Cheat Sheet": """🔹 **Concave Mirror:** Converging. <br>🔹 **Convex Mirror:** Diverging (Rear view). <br>🔹 **Snell's Law:** n = sin i / sin r. <br>🔹 **Power:** Unit is Dioptre (D).""",
            "Detailed Concepts": [
                "**Reflection:** ∠i = ∠r. Real vs Virtual images.",
                "**Mirror Formula:** Relationship between u, v, f.",
                "**Refraction:** Bending of light due to change in speed (c/v).",
                "**Lens:** Convex (Real) vs Concave (Always virtual/erect)."
            ],
            "Formulas": "• Mirror: 1/v + 1/u = 1/f <br>• Lens: 1/v - 1/u = 1/f <br>• Magnification: m = -v/u <br>• Power: P = 1/f(m)",
            "MCQs": ["Q1: Mirror used by dentists? Ans: Concave", "Q2: Power of Plane Mirror? Ans: 0"],
            "Diagrams": [{"title": "Refraction of Light", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Refraction_photo.png/300px-Refraction_photo.png"}]
        },
        "Ch 11: Electricity": {
            "Cheat Sheet": """🔹 **Ohm's Law:** V = IR. <br>🔹 **Ammeter:** In series. <br>🔹 **Voltmeter:** In parallel. <br>🔹 **Resistivity:** Constant for a material.""",
            "Detailed Concepts": [
                "**Electric Current:** Rate of flow of charge (Q/t).",
                "**Resistance:** Obstruction to current. R = ρ(L/A).",
                "**Combination:** Series (R = R1+R2) vs Parallel (1/R = 1/R1 + 1/R2).",
                "**Heating Effect:** H = I²Rt. Application in Bulb, Heater, Fuse."
            ],
            "Formulas": "• V = IR <br>• P = VI = I²R <br>• 1 kWh = 3.6 × 10⁶ J",
            "MCQs": ["Q1: Unit of Charge? Ans: Coulomb", "Q2: Unit of Power? Ans: Watt"],
            "Diagrams": [{"title": "Circuit Diagram", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ohm%27s_law_setup.svg/300px-Ohm%27s_law_setup.svg.png"}]
        }
    }
}

# --- LOGIC TO DISPLAY ---
st.markdown('<p class="main-title">🎓 Class 10 Science Digital Guru</p>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("📚 Library")
subject = st.sidebar.selectbox("Select Subject", list(syllabus_data.keys()))
chapter = st.sidebar.selectbox("Select Chapter", list(syllabus_data[subject].keys()))
mode = st.sidebar.radio("Learning Module", ["📖 Concepts", "⚡ Quick Cheat Sheet", "🔢 Formulas", "🖼️ Diagrams", "✍️ MCQs"])

# Content
chap_content = syllabus_data[subject][chapter]

if mode == "📖 Concepts":
    st.markdown(f"<h2 class='chap-header'>Detailed Concepts: {chapter}</h2>", unsafe_allow_html=True)
    for concept in chap_content["Detailed Concepts"]:
        st.markdown(f"<div class='concept-card'>{concept}</div>", unsafe_allow_html=True)
