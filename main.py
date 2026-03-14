import streamlit as st
import google.generativeai as genai

# Configuratie: Zorg dat je een API KEY hebt van Google AI Studio
# In een echte serveromgeving gebruik je st.secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Didactiek Coach", layout="wide")

# Systeemprompt
SYSTEM_PROMPT = """SYSTEM_PROMPT = """Je bent de PXL Didactiek Coach. 
Hanteer bij elke feedback de volgende structuur:
1. **Sterke punten:** Wat sluit goed aan bij de PXL-didactiek?
2. **Kritische reflectie:** Stel 1 socratische vraag over de aansluiting bij de 12 bouwstenen of de Bloom-taxonomie.
3. **Didactische tip:** Geef een concrete aanwijzing voor de volgende fase.

Wees bemoedigend maar scherp. Geef nooit direct het antwoord, maar laat de student zelf nadenken."""
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
