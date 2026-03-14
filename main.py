import streamlit as st
import google.generativeai as genai

# Configuratie
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="PXL Didactiek Coach", layout="wide")

# Verbeterde Systeemprompt
SYSTEM_PROMPT = """Je bent de PXL Didactiek Coach. 
Hanteer bij elke feedback de volgende structuur:
1. **Sterke punten:** Wat sluit goed aan bij de PXL-didactiek?
2. **Kritische reflectie:** Stel 1 socratische vraag over de aansluiting bij de 12 bouwstenen of de Bloom-taxonomie.
3. **Didactische tip:** Geef een concrete aanwijzing voor de volgende fase.

Wees bemoedigend maar scherp. Geef nooit direct het antwoord, maar laat de student zelf nadenken."""

st.title("PXL Didactiek Coach 🎓")

# Fase selectie en voortgangsbalk
fases = ["Identificatie", "Beginsituatie", "Lesdoelen", "Lesuitwerking", "Lesschema"]
fase = st.selectbox("Kies de fase waar je aan werkt", fases)

# Voortgangsbalk berekenen
progress = (fases.index(fase) + 1) / len(fases)
st.progress(progress)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Input: {fase}")
    user_input = st.text_area("Vul hier je tekst in:", height=300)
    if st.button("Vraag feedback aan de coach"):
        with st.spinner('De coach denkt na...'):
            try:
                response = model.generate_content(SYSTEM_PROMPT + "\n\nFase: " + fase + "\nInput: " + user_input)
                st.session_state.feedback = response.text
            except Exception as e:
                st.error(f"Er ging iets mis: {e}")

with col2:
    st.subheader("Feedback van de PXL Coach")
    if 'feedback' in st.session_state:
        st.markdown(st.session_state.feedback)
    else:
        st.info("Kies een fase, vul je tekst in en klik op de knop voor didactisch advies.")
