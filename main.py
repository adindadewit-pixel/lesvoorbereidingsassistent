import streamlit as st
import google.generativeai as genai
from kennisbank import KNOWLEDGE_BASE  # Zorg dat je kennisbank.py dit gebruikt

# Configuratie
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
try:
    models = genai.list_models()
    for m in models:
        st.write(f"Beschikbaar model: {m.name}")
except Exception as e:
    st.error(f"Fout bij verbinden met Google AI: {e}")

def geef_tussentijdse_feedback(sectie, input_data):
    # Haal de specifieke theorie op uit je KNOWLEDGE_BASE
    theorie = KNOWLEDGE_BASE.get(sectie, "Toets aan de algemene didactische PXL-normen.")
    
    prompt = f"""
    Je bent de PXL Didactiek Coach. Beoordeel de volgende input voor de sectie '{sectie}':
    
    RICHTLIJNEN: {theorie}
    STUDENT INPUT: {input_data}
    
    Geef je feedback in de vorm van:
    1. **Sterkte**: Wat voldoet er al aan de PXL-normen?
    2. **Ontbreekt**: Wat mis je op basis van de theorie?
    3. **Socratische vraag**: Stel één verdiepende vraag die de student dwingt de cursustekst beter te gebruiken.
    """
    
    response = model.generate_content(prompt)
    return response.text

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
        praktisch = st.text_area("Praktisch (lokaal, materiaal)", value=st.session_state.data.get('praktisch', ''))
        leerling = st.text_area("Leerlingkenmerken", value=st.session_state.data.get('leerling', ''))
        if st.form_submit_button("Feedback op Beginsituatie"):
            st.session_state.data.update({'praktisch': praktisch, 'leerling': leerling})
            with st.spinner("Analyseert..."):
                st.info(geef_tussentijdse_feedback("beginsituatie", f"{praktisch} {leerling}"))

# --- Stap 2 ---
elif stap == "2. Leerdoelen & Leerplan":
    with st.form("stap2"):
        cognitief = st.text_area("Cognitieve doelen (onderstreep werkwoorden)", value=st.session_state.data.get('cognitief', ''))
        if st.form_submit_button("Feedback op Leerdoelen"):
            st.session_state.data['cognitief'] = cognitief
            with st.spinner("Toetst aan Bloom..."):
                st.info(geef_tussentijdse_feedback("leerdoelen", cognitief))

# --- Stap 3 ---
elif stap == "3. Lesuitwerking":
    with st.form("stap3"):
        aanknoping = st.text_area("Aanknoping (Motivatie/Voorkennis)", value=st.session_state.data.get('fase_aanknoping', ''))
        uitvoering = st.text_area("Uitvoering (Kern/Bouwstenen)", value=st.session_state.data.get('fase_uitvoering', ''))
        afronding = st.text_area("Afronding (Consolidatie)", value=st.session_state.data.get('fase_afronding', ''))
        if st.form_submit_button("Feedback op Uitwerking"):
            st.session_state.data.update({'fase_aanknoping': aanknoping, 'fase_uitvoering': uitvoering, 'fase_afronding': afronding})
            with st.spinner("Toetst aan H6 en Bouwstenen..."):
                st.info(geef_tussentijdse_feedback("lesuitwerking", f"{aanknoping} {uitvoering} {afronding}"))

# --- Stap 4 ---
elif stap == "4. Lesschema & Bronnen":
    if st.button("Genereer definitief didactisch advies"):
        full_context = "\n\n".join(KNOWLEDGE_BASE.values())
        prompt = f"Geef een integraal advies op basis van deze data: {st.session_state.data}\n\nRichtlijnen: {full_context}"
        with st.spinner('De coach analyseert de volledige voorbereiding...'):
            st.markdown("### Feedback van de PXL Coach")
            st.write(model.generate_content(prompt).text)
