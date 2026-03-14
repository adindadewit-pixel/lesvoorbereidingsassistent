import streamlit as st
import google.generativeai as genai
from kennisbank import DIDACTISCHE_CONTEXT # Deze regel verbindt de twee bestanden

# Configuratie
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Lesvoorbereiding", layout="wide")

# PXL Huisstijl
st.markdown("""
    <style>
    body { font-family: Arial, sans-serif; color: #030203; }
    h1, h2 { font-family: 'Arial Black', sans-serif; color: #030203; text-transform: uppercase; }
    h1 { border-bottom: 3px solid #AE9A64; }
    .stButton>button { background-color: #AE9A64; color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("PXL Lesvoorbereidingsformulier 🎓")

if 'data' not in st.session_state:
    st.session_state.data = {}

stap = st.radio("Navigeer door het sjabloon:", 
                ["1. Identificatie & Beginsituatie", "2. Leerdoelen & Leerplan", "3. Lesuitwerking", "4. Lesschema & Bronnen"])

# [Hier staan je huidige if/elif stap 1 t/m 3 blokken - die blijven ongewijzigd!]

elif stap == "4. Lesschema & Bronnen":
    st.session_state.data['schema'] = st.text_area("Lesschema (Kern van de les)")
    st.session_state.data['bronnen'] = st.text_area("Leermiddelen & Geraadpleegde bronnen (APA)")
    
    if st.button("Genereer didactisch advies"):
        # Hier bouwen we de context op uit de kennisbank
        full_context = "\n".join(DIDACTISCHE_CONTEXT.values())
        
        system_prompt = f"""Je bent de PXL Didactiek Coach. Toets de input aan deze richtlijnen:
        {full_context}
        Geef socratische feedback, benoem concrete bouwstenen en check de beginsituatie.
        """
        
        prompt = f"{system_prompt}\n\nInput van student: {st.session_state.data}"
        
        with st.spinner('De coach analyseert op basis van de cursusteksten...'):
            response = model.generate_content(prompt)
            st.markdown("### Feedback van de PXL Coach")
            st.write(response.text)
