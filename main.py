import streamlit as st
import google.generativeai as genai

# Configuratie: Zorg dat je een API KEY hebt van Google AI Studio
# In een echte serveromgeving gebruik je st.secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Didactiek Coach", layout="wide")

# Systeemprompt
SYSTEM_PROMPT = """Je bent de PXL Didactiek Coach. Begeleid studenten bij het invullen van 
hun lesvoorbereidingsformulier (LVF). Baseer je strikt op de PXL-didactiek:
- Gebruik de 12 bouwstenen (Wijze Lessen) voor de uitvoeringsfase.
- Gebruik de taxonomie van Bloom voor doelen.
- Analyseer de beginsituatie op socio-cultureel, pedagogisch en vakinhoudelijk vlak.
- Wees socratisch: stel vragen, geef niet direct het antwoord.
"""

st.title("PXL Didactiek Coach 🎓")
st.markdown("Begeleiding bij het opstellen van je lesvoorbereiding.")

# Fase selectie
fase = st.sidebar.selectbox("Kies de fase waar je aan werkt", 
    ["Identificatie", "Beginsituatie", "Lesdoelen", "Lesuitwerking", "Lesschema"])

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Input: {fase}")
    user_input = st.text_area("Vul hier je tekst in:", height=300)
    if st.button("Vraag feedback aan de coach"):
        with st.spinner('De coach denkt na...'):
            response = model.generate_content(SYSTEM_PROMPT + "\n\nFase: " + fase + "\nInput: " + user_input)
            st.session_state.feedback = response.text

with col2:
    st.subheader("Feedback van de PXL Coach")
    if 'feedback' in st.session_state:
        st.markdown(st.session_state.feedback)
    else:
        st.info("Kies een fase, vul je tekst in en klik op de knop voor didactisch advies.")
