import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- CSS STYLING ---
st.markdown("""
    <style>
    /* Hintergrundfarbe der App */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Design des Buttons */
    div.stButton > button {
        background-color: #004a99;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        width: 100%;
        height: 50px;
    }
    /* Schriftart anpassen */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    /* Ergebnis-Box schöner machen */
    .stSuccess {
        background-color: #e1f5fe;
        border: 1px solid #b3e5fc;
        color: #01579b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. KONFIGURATION ---
# Versucht, den Key aus den Streamlit-Secrets (Cloud) oder der Umgebung (lokal) zu laden
try:
    # In der Cloud: st.secrets["API_KEY"]
    # Lokal: os.environ.get("API_KEY")
    api_key = st.secrets.get("API_KEY") or os.environ.get("API_KEY")
    
    if not api_key:
        raise Exception("API Key nicht gefunden!")
        
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Konfigurationsfehler: {e}. Bitte stelle sicher, dass der API_KEY gesetzt ist.")
    st.stop()

# --- 2. DESIGN & LAYOUT ---
st.set_page_config(page_title="BIM Katalog", page_icon="📚", layout="centered")
st.title("📚 BIM Publikations-Finder")
st.write("Beschreiben Sie Ihre Herausforderung. Unsere KI analysiert den Katalog.")
st.divider()

# --- 3. DATEN LADEN ---
@st.cache_data
def lade_katalog():
    return pd.read_csv("katalog.csv")

try:
    df = lade_katalog()
    katalog_text = df.to_string(index=False)
except Exception as e:
    st.error(f"Katalog-Datei 'katalog.csv' konnte nicht geladen werden: {e}")
    st.stop()

# --- 4. NUTZEREINGABE ---
problem_beschreibung = st.text_area("Wo hakt es in Ihrem Projekt?", height=150)

# --- 5. KI-LOGIK ---
if st.button("Passende Lösung finden"):
    if problem_beschreibung:
        with st.spinner("Katalog wird durchsucht..."):
            system_prompt = f"""
            Du bist der fachliche Berater für BIM-Publikationen.
            Hier ist unser aktueller Katalog:
            {katalog_text}

            DEINE REGELN:
            1. Empfiehl NUR Bücher aus der Liste oben. Erfinde nichts!
            2. Wenn das Problem nicht passt, sage, dass wir dazu keine Publikation haben.
            3. Antworte in 3-4 Sätzen und nenne den Titel in **Fett** sowie den Link.

            Herausforderung des Nutzers: {problem_beschreibung}
            """
            
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(system_prompt)
                st.success(response.text)
            except Exception as e:
                st.error(f"Fehler bei der KI-Anfrage: {e}")
    else:
        st.warning("Bitte beschreiben Sie zuerst Ihr Problem.")
