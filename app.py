import streamlit as st

# --- UI CONFIG ---
st.set_page_config(page_title="Class 10 Science Hub 2026-27", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR COLORFUL TEXT ---
st.markdown("""
    <style>
    .main-title { font-size:50px; color: #FF4B4B; font-weight: bold; text-align: center; }
    .cheat-sheet-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #00c0f2; }
    .highlight-blue { color: #00c0f2; font-weight: bold; }
    .highlight-green { color: #28a745; font-weight: bold; }
    .highlight-orange { color: #fd7e14; font-weight: bold; }
    </style>
    """, unsafe_allow_stdio=True)

# --- THE MEGA DATASET ---
data = {
    "🧪 Chemistry": {
        "1. Chemical Reactions & Equations": {
            "Cheat Sheet": "✨ **Key Law:** Law of Conservation of Mass. <br>🌈 **Colors:** AgCl (White), AgBr (Yellow), CuO (Black), FeSO4 (Green).",
            "Formulas": "• Combination: A + B → AB <br>• Decomposition: AB → A + B <br>• Displacement: A + BC → AC + B",
            "Concepts": "Focus on balancing equations and identifying Redox (Oxidation & Reduction).",
            "MCQs": ["1. Burning of Magnesium ribbon is? Ans: Combination & Exothermic", "2. What is Rust? Ans: Hydrated Ferric Oxide"],
            "Diagrams": [{"title": "Electrolysis of Water", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Electrolysis_of_water.svg/300px-Electrolysis_of_water.svg.png"}]
        },
        "2. Acids, Bases & Salts": {
            "Cheat Sheet": "🍋 **Acids:** Turn Blue Litmus Red. 🧼 **Bases:** Turn Red Litmus Blue. <br>🌡️ **pH:** <7 Acid, 7 Neutral, >7 Base.",
            "Formulas": "• pH = -log[H+] <br>• Acid + Base → Salt + Water <br>• Bleaching Powder: CaOCl2 <br>• Baking Soda: NaHCO3",
            "Concepts": "Importance of pH in daily life (Tooth decay starts at 5.5). Chlor-alkali process.",
            "MCQs": ["1. pH of Gastric juice? Ans: 1.2", "2. Acid in Ants? Ans: Methanoic Acid"],
            "Diagrams": [{"title": "pH Scale", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PH_Scale.svg/400px-PH_Scale.svg.png"}]
        },
        "3. Metals & Non-Metals": {
            "Cheat Sheet": "🔥 **Reactivity:** K > Na > Ca > Mg > Al... <br>💎 **Ionic Bonds:** High melting point, conduct in water.",
            "Formulas": "• Roasting: Metal Sulphide + O2 → Metal Oxide + SO2 <br>• Calcination: Metal Carbonate → Metal Oxide + CO2",
            "Concepts": "Amphoteric oxides (Al2O3), Aqua Regia (3:1 HCl:HNO3), and Corrosion prevention.",
            "MCQs": ["1. Liquid metal? Ans: Mercury", "2. Best conductor? Ans: Silver"],
            "Diagrams": [{"title": "Electrolytic Refining", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Electrolytic_refining_of_copper.png/300px-Electrolytic_refining_of_copper.png"}]
        },
        "4. Carbon & Its Compounds": {
            "Cheat Sheet": "🔗 **Tetravalency:** Carbon makes 4 bonds. <br>🦄 **Allotropes:** Diamond, Graphite, Fullerene.",
            "Formulas": "• Alkanes: CnH2n+2 <br>• Alkenes: CnH2n <br>• Alkynes: CnH2n-2 <br>• Ethanol: C2H5OH",
            "Concepts": "Saturated (Single bond) vs Unsaturated (Double/Triple). Saponification vs Esterification.",
            "MCQs": ["1. Simplest hydrocarbon? Ans: Methane", "2. Functional group -OH? Ans: Alcohol"],
            "Diagrams": [{"title": "Micelle Formation", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Micelle_scheme-en.svg/300px-Micelle_scheme-en.svg.png"}]
        }
    },
    "🧬 Biology": {
        "5. Life Processes": {
            "Cheat Sheet": "🍎 **Nutrition:** Villi absorb food. <br>🫁 **Respiration:** Mitochondria is the powerhouse. <br>🩸 **Circulation:** Double Pump system.",
            "Formulas": "• Photosynthesis: 6CO2 + 12H2O → C6H12O6 + 6O2 + 6H2O <br>• ATP: Energy Currency",
            "Concepts": "Breakdown of glucose in cytoplasm vs mitochondria. Role of Nephrons in kidneys.",
            "MCQs": ["1. Site of photosynthesis? Ans: Chloroplast", "2. Instrument for Blood Pressure? Ans: Sphygmomanometer"],
            "Diagrams": [{"title": "Human Heart", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/300px-Diagram_of_the_human_heart_%28cropped%29.svg.png"}]
        },
        "6. Control & Coordination": {
            "Cheat Sheet": "🧠 **Brain:** Forebrain (Thinking), Hindbrain (Posture). <br>🌿 **Plants:** Auxin (Growth), Abscisic Acid (Stop).",
            "Formulas": "• Synapse: Gap between neurons. <br>• Reflex Arc: Receptor → Sensory → Spinal Cord → Motor → Effector.",
            "Concepts": "Endocrine glands: Insulin (Pancreas), Adrenaline (Adrenal), Growth Hormone (Pituitary).",
