import streamlit as st
import google.generativeai as genai

# Configuratie
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Lesvoorbereiding", layout="wide")

# PXL Huisstijl (CSS)
st.markdown("""
    <style>
    body { font-family: Arial, sans-serif; color: #030203; }
    h1, h2 { font-family: 'Arial Black', sans-serif; color: #030203; text-transform: uppercase; }
    h1 { border-bottom: 3px solid #AE9A64; }
    .stButton>button { background-color: #AE9A64; color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("PXL Lesvoorbereidingsformulier 🎓")

# Sessie-state om data te onthouden tussen stappen
if 'data' not in st.session_state:
    st.session_state.data = {}

# Menu voor navigatie door het sjabloon
stap = st.radio("Navigeer door het sjabloon:", 
                ["1. Identificatie & Beginsituatie", "2. Leerdoelen & Leerplan", "3. Lesuitwerking", "4. Lesschema & Bronnen"])

# Stap 1: Identificatie & Beginsituatie [cite: 177, 178]
if stap == "1. Identificatie & Beginsituatie":
    with st.form("stap1"):
        st.subheader("Identificatie van de les")
        st.session_state.data['school'] = st.text_input("School")
        st.session_state.data['leervak'] = st.text_input("Leervak")
        st.session_state.data['onderwerp'] = st.text_input("Lesonderwerp")
        
        st.subheader("Didactische beginsituatie")
        st.session_state.data['praktisch'] = st.text_area("Praktisch (lokaal, materiaal, ...)")
        st.session_state.data['leerling'] = st.text_area("Leerling (interesses, relaties, problemen)")
        st.session_state.data['vakinhoud'] = st.text_area("Vakinhoudelijk (voorkennis, ervaring)")
        st.form_submit_button("Opslaan")

# Stap 2: Leerdoelen & Leerplan [cite: 179, 180]
elif stap == "2. Leerdoelen & Leerplan":
    with st.form("stap2"):
        st.subheader("Situering in leerplan")
        st.session_state.data['leerplan'] = st.text_input("Geraadpleegd leerplan (titel/nummer)")
        
        st.subheader("Lesdoelen (Bloom)")
        st.session_state.data['cognitief'] = st.text_area("Cognitief (+ ref leerplandoel)")
        st.session_state.data['psycho'] = st.text_area("Psychomotorisch (+ ref leerplandoel)")
        st.session_state.data['affectief'] = st.text_area("Affectief (+ ref leerplandoel)")
        st.form_submit_button("Opslaan")

# Stap 3: Lesuitwerking 
elif stap == "3. Lesuitwerking":
    st.info("Vul per lesfase de kolommen in: DW, LM, DB, DF, LKR/LL gedrag.")
    st.session_state.data['uitwerking'] = st.text_area("Gedetailleerde Lesuitwerking (Aanknoping, Uitvoering, Afronding)", height=400)

# Stap 4: Lesschema, Bronnen & Feedback [cite: 183, 185]
elif stap == "4. Lesschema & Bronnen":
    st.session_state.data['schema'] = st.text_area("Lesschema (Kern van de les)")
    st.session_state.data['bronnen'] = st.text_area("Leermiddelen & Geraadpleegde bronnen (APA)")
    
    if st.button("Genereer didactisch advies"):
        # Hier wordt alle data gecombineerd en naar de AI gestuurd
        prompt = f"Analyseer deze lesvoorbereiding op basis van de PXL-kijkwijzer: {st.session_state.data}"
        response = model.generate_content(prompt)
        st.markdown("### Feedback van de PXL Coach")
        st.write(response.text)
