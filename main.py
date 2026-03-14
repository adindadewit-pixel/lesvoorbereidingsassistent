import streamlit as st
import google.generativeai as genai
from kennisbank import KNOWLEDGE_BASE  # Zorg dat je kennisbank.py dit gebruikt

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

# --- Stap 1 ---
if stap == "1. Identificatie & Beginsituatie":
    with st.form("stap1"):
        st.subheader("Didactische beginsituatie")
        st.session_state.data['praktisch'] = st.text_area("Praktisch (lokaal, materiaal)")
        st.session_state.data['leerling'] = st.text_area("Leerlingkenmerken (sociaal, motivatie, taal)")
        st.session_state.data['vakinhoud'] = st.text_area("Vakinhoudelijk (voorkennis, metacognitie)")
        st.form_submit_button("Opslaan")

# --- Stap 2 ---
elif stap == "2. Leerdoelen & Leerplan":
    with st.form("stap2"):
        st.subheader("Lesdoelen (Bloom)")
        st.session_state.data['cognitief'] = st.text_area("Cognitief (+ ref leerplandoel, onderstreep handelingswerkwoord)")
        st.session_state.data['psycho_affectief'] = st.text_area("Psychomotorisch & Affectief")
        st.form_submit_button("Opslaan")

# --- Stap 3: Gestructureerde Fasering (H6) ---
elif stap == "3. Lesuitwerking":
    st.subheader("Gedetailleerde Lesuitwerking (H6)")
    with st.form("stap3"):
        st.session_state.data['fase_aanknoping'] = st.text_area("1. Aanknoping (Motivatie, voorkennis, doelstelling)", height=150)
        st.session_state.data['fase_uitvoering'] = st.text_area("2. Uitvoering (Kern, actieve verwerking, differentiatie)", height=250)
        st.session_state.data['fase_afronding'] = st.text_area("3. Afronding (Consolidatie, herhaling, vooruitblik)", height=150)
        st.form_submit_button("Opslaan lesuitwerking")

# --- Stap 4: Analyse & Feedback ---
elif stap == "4. Lesschema & Bronnen":
    st.session_state.data['schema'] = st.text_area("Lesschema (Kern van de les)")
    st.session_state.data['bronnen'] = st.text_area("Leermiddelen (APA)")
    
    if st.button("Genereer didactisch advies"):
        # Alle kennis uit kennisbank.py ophalen
        complete_context = "\n\n".join(KNOWLEDGE_BASE.values())
        
        system_prompt = f"""
        Je bent de PXL Didactiek Coach. Analyseer de lesvoorbereiding op basis van:
        {complete_context}
        
        GEEF PER FASE FEEDBACK:
        1. AANKNOPING: Wordt voorkennis geactiveerd? Is het doel helder voor de leerling?
        2. UITVOERING: Worden de 12 bouwstenen toegepast? Is er differentiatie (UDL/CLIM)? 
           Is de cognitieve belasting optimaal?
        3. AFRONDING: Geen nieuwe leerstof! Is het consolidatiemoment (bordschema) duidelijk?
        
        CHECK LEERDOELEN: Zijn de handelingswerkwoorden onderstreept en gekoppeld aan leerplannummers?
        
        STIJL: Socratisch. Stel vragen die de student helpen kritisch na te denken.
        """
        
        prompt = f"{system_prompt}\n\nINPUT STUDENT: {st.session_state.data}"
        
        with st.spinner('De coach analyseert op basis van de cursusteksten...'):
            response = model.generate_content(prompt)
            st.markdown("### Feedback van de PXL Coach")
            st.write(response.text)
