import streamlit as st

# --- UI CONFIG ---
st.set_page_config(page_title="Class 10 Science Hub 2026-27", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR DESIGN ---
st.markdown("""
    <style>
    .main-title { font-size:45px; color: #FF4B4B; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .cheat-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 6px solid #00c0f2; margin-bottom: 15px; }
    .formula-box { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 6px solid #2e7d32; margin-bottom: 15px; }
    .highlight { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_stdio=True)

# --- THE COMPLETE DATASET (ALL 13 CHAPTERS) ---
data = {
    "🧪 Chemistry": {
        "Ch 1: Chemical Reactions": {
            "Cheat Sheet": "🌈 **Colors:** AgCl (White), CuO (Black), FeSO4 (Green). <br>⚖️ **Law:** Mass is neither created nor destroyed.",
            "Formulas": "• Combination: A + B → AB <br>• Decomposition: AB → A + B <br>• Redox: Oxidation (Loss of e-) & Reduction (Gain of e-)",
            "Concepts": "Types of reactions: Combination, Decomposition, Displacement, Double Displacement, Oxidation, and Reduction.",
            "MCQs": ["1. Fe2O3 + 2Al → Al2O3 + 2Fe is? Ans: Displacement", "2. Respiration is? Ans: Exothermic"],
            "Diagrams": [{"title": "Electrolysis of Water", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Electrolysis_of_water.svg/300px-Electrolysis_of_water.svg.png"}]
        },
        "Ch 2: Acids, Bases & Salts": {
            "Cheat Sheet": "🍋 **pH < 7:** Acid (H+ ions). <br>🧼 **pH > 7:** Base (OH- ions). <br>🦷 **Tooth Decay:** Starts at pH 5.5.",
            "Formulas": "• Acid + Base → Salt + Water <br>• Bleaching Powder: CaOCl2 <br>• Baking Soda: NaHCO3 <br>• Plaster of Paris: CaSO4.1/2H2O",
            "Concepts": "Indicators (Litmus, Phenolphthalein), pH scale, and chemicals from common salt.",
            "MCQs": ["1. Acid in Tomato? Ans: Oxalic Acid", "2. pH of blood? Ans: 7.4"],
            "Diagrams": [{"title": "pH Scale", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PH_Scale.svg/400px-PH_Scale.svg.png"}]
        },
        "Ch 3: Metals & Non-Metals": {
            "Cheat Sheet": "🔥 **Amphoteric Oxides:** Act as both acid/base (Al2O3). <br>💎 **Ionic Bond:** Metal + Non-metal transfer electrons.",
            "Formulas": "• Roasting: Sulphide ore + O2 + Heat <br>• Calcination: Carbonate ore + Heat",
            "Concepts": "Reactivity series, properties of ionic compounds, metallurgy, and corrosion.",
            "MCQs": ["1. Liquid metal? Ans: Mercury", "2. Best conductor? Ans: Silver"],
            "Diagrams": [{"title": "Reactivity Series", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Electrolytic_refining_of_copper.png/300px-Electrolytic_refining_of_copper.png"}]
        },
        "Ch 4: Carbon & Its Compounds": {
            "Cheat Sheet": "🔗 **Catenation:** Carbon's ability to form long chains. <br>🧼 **Saponification:** Making soap from esters.",
            "Formulas": "• Alkanes: CnH2n+2 <br>• Alkenes: CnH2n <br>• Alkynes: CnH2n-2",
            "Concepts": "Functional groups, Homologous series, Combustion, Oxidation, Addition, and Substitution reactions.",
            "MCQs": ["1. Valency of Carbon? Ans: 4", "2. Hardest Allotrope? Ans: Diamond"],
            "Diagrams": [{"title": "Electron Dot Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Micelle_scheme-en.svg/300px-Micelle_scheme-en.svg.png"}]
        }
    },
    "🧬 Biology": {
        "Ch 5: Life Processes": {
            "Cheat Sheet": "🍎 **Autotrophic:** Plants. **Heterotrophic:** Humans. <br>🫁 **Alveoli:** Site of gas exchange in lungs.",
            "Formulas": "• Aerobic Respiration: Glucose + O2 → CO2 + H2O + Energy (38 ATP)",
            "Concepts": "Nutrition, Respiration, Transportation (Heart), and Excretion (Kidneys/Nephrons).",
            "MCQs": ["1. Pumping organ? Ans: Heart", "2. Structural unit of Kidney? Ans: Nephron"],
            "Diagrams": [{"title": "Human Heart", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/300px-Diagram_of_the_human_heart_%28cropped%29.svg.png"}]
        },
        "Ch 6: Control & Coordination": {
            "Cheat Sheet": "🧠 **Cerebrum:** Main thinking part. <br>🌿 **Geotropism:** Response to Gravity.",
            "Formulas": "• Reflex Arc: Stimulus → Receptor → Spinal Cord → Effector",
            "Concepts": "Nervous system, Reflex action, Plant hormones (Auxin, Gibberellin), and Animal hormones.",
            "MCQs": ["1. master Gland? Ans: Pituitary", "2. Gap between neurons? Ans: Synapse"],
            "Diagrams": [{"title": "Neuron Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Blausen_0657_MultipolarNeuron.png/300px-Blausen_0657_MultipolarNeuron.png"}]
        },
        "Ch 7: Reproduction": {
            "Cheat Sheet": "🍓 **Asexual:** Clone produced. <br>🌸 **Stamen:** Male part. **Carpel:** Female part.",
            "Formulas": "• Fission (Amoeba) <br>• Budding (Hydra) <br>• Regeneration (Planaria)",
            "Concepts": "Asexual vs Sexual reproduction, Human reproductive system, and Contraceptive methods.",
            "MCQs": ["1. Pollen is produced in? Ans: Anther", "2. Copper-T is? Ans: Contraceptive"],
            "Diagrams": [{"title": "Flower Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Mature_flower_diagram.svg/300px-Mature_flower_diagram.svg.png"}]
        },
        "Ch 8: Heredity": {
            "Cheat Sheet": "🧬 **DNA:** Carrier of info. <br>👨‍🔬 **Mendel:** Father of Genetics (used Pea plants).",
            "Formulas": "• Monohybrid Ratio (F2): 3:1 <br>• Dihybrid Ratio (F2): 9:3:3:1",
            "Concepts": "Genotype vs Phenotype, Sex determination in humans (XY system).",
            "MCQs": ["1. XX chromosome means? Ans: Female", "2. Basic unit of heredity? Ans: Gene"],
            "Diagrams": [{"title": "Sex Determination", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Human_chromosomes_XX_and_XY.png/300px-Human_chromosomes_XX_and_XY.png"}]
        }
    },
    "⚡ Physics": {
        "Ch 9: Light": {
            "Cheat Sheet": "🪞 **Concave Mirror:** Used by dentists. <br>🔍 **Refraction:** Bending of light.",
            "Formulas": "• Mirror: 1/v + 1/u = 1/f <br>• Lens: 1/v - 1/u = 1/f <br>• Power: P = 1/f(m)",
            "Concepts": "Reflection laws, Spherical mirrors, Lens formula, and Magnification.",
            "MCQs": ["1. Unit of Power? Ans: Dioptre", "2. Virtual/Erect image? Ans: Convex Mirror"],
            "Diagrams": [{"title": "Ray
