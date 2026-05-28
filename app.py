import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- 1. KONFIGURATION ---
try:
    api_key = st.secrets.get("API_KEY") or os.environ.get("API_KEY")
    if not api_key:
        raise Exception("API Key nicht gefunden!")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Konfigurationsfehler: {e}")
    st.stop()

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-family: 'Favourit Pro', sans-serif !important;
        color: #032B5E !important;
    }
    .stApp { background-color: #FFFFFF; }
    [data-baseweb="textarea"] {
        background-color: #FFFFFF !important;
        border: 2px solid #032B5E !important;
        color: #032B5E !important;
    }
    div.stButton > button {
        background-color: #032B5E !important;
        color: #FFFFFF !important;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        width: 100%;
        height: 50px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #EC1616 !important;
        color: #FFFFFF !important;
    }
    h1 { color: #032B5E !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIK & LAYOUT ---
st.title("📚 BIM Publikations-Finder")
st.write("Beschreiben Sie Ihre Herausforderung. Unsere KI analysiert den Katalog.")
st.divider()

@st.cache_data
def lade_katalog():
    return pd.read_csv("katalog.csv")

try:
    df = lade_katalog()
    katalog_text = df.to_string(index=False)
except:
    st.error("Katalog-Datei 'katalog.csv' nicht gefunden!")
    st.stop()

# Session State für Textfeld
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

def clear_text():
    st.session_state.input_text = ""

problem_beschreibung = st.text_area(
    "Wo hakt es in Ihrem Projekt?", 
    value=st.session_state.input_text,
    key="input_field",
    height=150
)

# Buttons nebeneinander
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Löschen"):
        st.session_state.input_text = ""
        st.rerun()

with col2:
    if st.button("Passende Lösung finden"):
        if problem_beschreibung:
            with st.spinner("Katalog wird durchsucht..."):
                system_prompt = f"""
                Du bist der fachliche Berater für BIM-Publikationen.
                Hier ist unser aktueller Katalog:
                {katalog_text}

                DEINE REGELN:
                1. Empfiehl NUR Bücher aus der Liste oben.
                2. Wenn nichts passt, antworte freundlich, dass wir dazu keine Publikation haben.
                3. Antworte in 3-4 Sätzen. Nenne den Titel in **Fett** sowie den Link.

                Herausforderung: {problem_beschreibung}
                """
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(system_prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Fehler: {e}")
        else:
            st.warning("Bitte geben Sie zuerst ein Problem ein.")
