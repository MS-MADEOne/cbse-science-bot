import streamlit as st

# --- DATASET (Sample - You can expand this) ---
import streamlit as st

# --- COMPREHENSIVE CBSE 10th PHYSICS DATA ---
data = {
    "Physics": {
        "Light: Reflection & Refraction": {
            "Concepts": """
            **1. Reflection:** Bouncing back of light. Laws: ∠i = ∠r; Incident, reflected ray & normal lie in the same plane.
            **2. Spherical Mirrors:** Concave (Converging) and Convex (Diverging).
            **3. Mirror Formula:** 1/v + 1/u = 1/f.
            **4. Refraction:** Bending of light when traveling from one medium to another. n = c/v.
            **5. Lens Formula:** 1/v - 1/u = 1/f. 
            **6. Power of Lens:** P = 1/f (in meters). Unit: Dioptre (D).
            """,
            "MCQs": [
                "1. Which mirror is used by dentists? \nAns: Concave Mirror",
                "2. The refractive index of water is 1.33. What does this mean? \nAns: Speed of light in air is 1.33 times faster than in water.",
                "3. Where should an object be placed to get a real image of the same size? \nAns: At 2F."
            ],
            "Very Short Answers (1M)": [
                "Q: Define Principal Focus. \nA: The point on the principal axis where all parallel light rays meet after reflection/refraction.",
                "Q: Write the sign convention for a concave mirror's focal length. \nA: Negative."
            ],
            "Short Answers (3M)": [
                "Q: State the laws of refraction. \nA: 1. Incident ray, refracted ray, and normal lie in the same plane. 2. Snell's Law: sin i / sin r = constant.",
                "Q: Why is a convex mirror used as a rear-view mirror? \nA: It gives an erect, diminished image and a wider field of view."
            ],
            "Long Answers (5M)": [
                "Q: Draw ray diagrams for a concave mirror when the object is between C and F. Describe the nature and size. \nA: Image is formed beyond C, it is real, inverted, and magnified."
            ],
            "Diagrams": [
                {"title": "Ray Diagrams (Concave Mirror)", "url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Reflection_angles.svg"},
                {"title": "Refraction through Glass Slab", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Refraction_photo.png/300px-Refraction_photo.png"}
            ]
        },
        "Human Eye & Colorful World": {
            "Concepts": """
            **1. Power of Accommodation:** Ability of the eye lens to adjust focal length.
            **2. Defects of Vision:** Myopia (Short-sightedness), Hypermetropia (Long-sightedness), Presbyopia.
            **3. Dispersion:** Splitting of white light into VIBGYOR through a prism.
            **4. Atmospheric Refraction:** Twinkling of stars, Advanced sunrise, Delayed sunset.
            **5. Tyndall Effect:** Scattering of light by colloidal particles.
            """,
            "MCQs": [
                "1. The least distance of distinct vision for a normal eye is? \nAns: 25 cm",
                "2. The red color of the sun at sunrise is due to? \nAns: Scattering of light."
            ],
            "Very Short Answers (1M)": [
                "Q: Which part of the eye controls the amount of light entering? \nA: Iris (by adjusting Pupil size).",
                "Q: What is the function of the Retina? \nA: It acts as a screen where images are formed and converted into electrical signals."
            ],
            "Short Answers (3M)": [
                "Q: Explain Myopia. \nA: Person can see nearby objects clearly but not distant ones. Image forms in front of the retina. Corrected by Concave lens."
            ],
            "Long Answers (5M)": [
                "Q: Describe the formation of a Rainbow. \nA: It is caused by dispersion, refraction, and internal reflection of sunlight by water droplets."
            ],
            "Diagrams": [
                {"title": "Human Eye Structure", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Schematic_diagram_of_the_human_eye_en.svg/400px-Schematic_diagram_of_the_human_eye_en.svg.png"},
                {"title": "Myopia and Correction", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Myopia.svg/300px-Myopia.svg.png"}
            ]
        },
        "Electricity": {
            "Concepts": """
            **1. Electric Current (I):** I = Q/t. Unit: Ampere.
            **2. Ohm’s Law:** V = IR (at constant temperature).
            **3. Resistance (R):** Depends on length (L), Area (A), and nature of material (ρ). R = ρL/A.
            **4. Series Connection:** Rs = R1 + R2 + R3.
            **5. Parallel Connection:** 1/Rp = 1/R1 + 1/R2 + 1/R3.
            **6. Joule’s Heating:** H = I²Rt.
            **7. Electric Power:** P = VI = I²R = V²/R.
            """,
            "MCQs": [
                "1. Unit of Resistivity is? \nAns: Ohm-meter (Ωm)",
                "2. If resistance is doubled, current becomes? \nAns: Half."
            ],
            "Very Short Answers (1M)": [
                "Q: Define 1 Ampere. \nA: Flow of 1 Coulomb of charge per second.",
                "Q: Why is Tungsten used in bulbs? \nA: High melting point."
            ],
            "Short Answers (3M)": [
                "Q: Distinguish between Series and Parallel circuits. \nA: Series: Same current, different voltage. Parallel: Different current, same voltage."
            ],
            "Long Answers (5M)": [
                "Q: Derive the expression for equivalent resistance in parallel. \nA: Use I = I1 + I2 + I3 and V/R = V/R1 + V/R2 + V/R3."
            ],
            "Diagrams": [
                {"title": "Ohm's Law Circuit", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ohm%27s_law_setup.svg/300px-Ohm%27s_law_setup.svg.png"}
            ]
        },
        "Magnetic Effects of Current": {
            "Concepts": """
            **1. Magnetic Field:** Region around a magnet where force is exerted.
            **2. Right Hand Thumb Rule:** Used to find direction of magnetic field around a straight conductor.
            **3. Solenoid:** A coil of many circular turns of insulated copper wire.
            **4. Fleming’s Left Hand Rule:** For direction of Force (Thump-Force, Forefinger-Field, Middle-Current).
            **5. Domestic Circuits:** Live wire (Red), Neutral wire (Black), Earth wire (Green). 220V, 50Hz in India.
            """,
            "MCQs": [
                "1. The device used to detect current is? \nAns: Galvanometer",
                "2. Direct Current (DC) frequency is? \nAns: 0 Hz"
            ],
            "Very Short Answers (1M)": [
                "Q: What is a magnetic field line? \nA: Imaginary paths along which a North pole would move.",
                "Q: What is the role of Fuse? \nA: Prevents damage from short-circuiting/overloading."
            ],
            "Short Answers (3M)": [
                "Q: List properties of magnetic field lines. \nA: 1. Start North, end South. 2. Never intersect. 3. Crowded at poles."
            ],
            "Long Answers (5M)": [
                "Q: Explain the working of a Solenoid. How can we increase its strength? \nA: By increasing the number of turns or increasing current or using a soft iron core."
            ],
            "Diagrams": [
                {"title": "Magnetic Field around Bar Magnet", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/VFPt_cylindrical_magnet_thumb.svg/300px-VFPt_cylindrical_magnet_thumb.svg.png"}
            ]
        }
    }
}

# --- IMPROVED UI LOGIC ---
st.set_page_config(page_title="CBSE Class 10 Science Bot", page_icon="🚀")
st.title("🚀 CBSE Class 10 Science Study Bot")

# Sidebar navigation
st.sidebar.header("Navigation")
subject = st.sidebar.selectbox("Subject", list(data.keys()))
chapter = st.sidebar.selectbox("Chapter", list(data[subject].keys()))
category = st.sidebar.radio("Resource Type", ["Concepts", "MCQs", "Very Short Answers (1M)", "Short Answers (3M)", "Long Answers (5M)", "Diagrams"])

# Display Section
st.header(f"{chapter}")
st.subheader(category)

selected_data = data[subject][chapter][category]

if category == "Diagrams":
    for diag in selected_data:
        st.write(f"**{diag['title']}**")
        st.image(diag['url'])
elif isinstance(selected_data, list):
    for item in selected_data:
        with st.expander("Show Question/Answer"):
            st.write(item)
else:
    st.info(selected_data)

# Footer
st.sidebar.divider()
st.sidebar.write("✅ **Syllabus:** CBSE 2024-25")
st.sidebar.write("👨‍🏫 **Target:** Class 10 Board Exams"),
    } }"Chemistry": {
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
