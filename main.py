import streamlit as st
import google.generativeai as genai

# Configuratie
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Lesvoorbereiding", layout="wide")

# --- PXL HUISSTIJL (CSS) ---
st.markdown("""
    <style>
    body { font-family: Arial, sans-serif; color: #030203; }
    h1, h2, h3 { font-family: 'Arial Black', sans-serif; color: #030203; text-transform: uppercase; }
    h1 { border-bottom: 3px solid #AE9A64; }
    .stButton>button { background-color: #AE9A64; color: white; border: none; font-weight: bold; }
    .stTextArea label { color: #030203; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("PXL Lesvoorbereidingsassistent 🎓")

# --- LOGICA & STRUCTUUR ---
# Structuur op basis van de Kijkwijzer [cite: 5, 9, 10, 96, 161]
with st.form("pxl_template"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Identificatie & Beginsituatie")
        school = st.text_input("School")
        lesonderwerp = st.text_input("Lesonderwerp")
        beginsituatie = st.text_area("Didactische beginsituatie (Praktisch, Leerling, Vakinhoudelijk) [cite: 10, 23]", height=150)
        
        st.subheader("2. Lesdoelen & Leerplan")
        doelen = st.text_area("Lesdoelen (Taxonomie van Bloom, CV/PV/AV) [cite: 96, 97]", height=150)
        
    with col2:
        st.subheader("3. Lesuitwerking")
        uitwerking = st.text_area("Aanknopings-, Uitvoerings- & Afrondingsfase [cite: 153, 157]", height=250)
        
        st.subheader("4. Lesschema")
        schema = st.text_area("Kern van de les (Bordschema/Kernwoorden) [cite: 161, 164]", height=150)
        
        submitted = st.form_submit_button("Genereer didactisch advies")

# --- FEEDBACK SYSTEEM ---
if submitted:
    SYSTEM_PROMPT = """Je bent de PXL Didactiek Coach. Analyseer de input op basis van de Kijkwijzer Lesvoorbereiding[cite: 5].
    Hanteer deze structuur:
    1. **Sterke punten:** Wat sluit goed aan bij de PXL-didactiek en bouwstenen? [cite: 120]
    2. **Kritische reflectie:** Stel 1 socratische vraag over de aansluiting bij de 12 bouwstenen of de Bloom-taxonomie[cite: 96, 120].
    3. **Didactische tip:** Geef een concrete aanwijzing voor verbetering.
    
    Wees bemoedigend maar scherp."""
    
    input_text = f"Beginsituatie: {beginsituatie}\nDoelen: {doelen}\nUitwerking: {uitwerking}\nSchema: {schema}"
    
    with st.spinner('De coach toetst aan de PXL-richtlijnen...'):
        response = model.generate_content(SYSTEM_PROMPT + "\n\nInput: " + input_text)
        st.markdown("### Feedback van de PXL Coach")
        st.write(response.text)
