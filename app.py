import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- 1. KONFIGURATION ---
# Wir holen den Key sicher aus den Streamlit-Secrets (in der Cloud)
# Für den lokalen Test kannst du st.secrets["API_KEY"] durch deinen echten String ersetzen
try:
    genai.configure(api_key=st.secrets["API_KEY"])
except:
    # Fallback für lokales Testen ohne Secrets-Datei:
    # Ersetze den String unten mit deinem tatsächlichen API-Key
    genai.configure(api_key="AIzaSyBJZvQAic1Im6JE0zk1aoucYz-lrS5k_28")

# --- 2. DESIGN & LAYOUT ---
st.set_page_config(page_title="BIM Katalog", page_icon="📚", layout="centered")

st.title("📚 BIM Publikations-Finder")
st.write("Beschreiben Sie Ihre aktuelle BIM-Herausforderung. Unsere KI analysiert Ihr Problem und empfiehlt die passende Publikation.")

st.divider()

# --- 3. DATEN LADEN ---
@st.cache_data
def lade_katalog():
    return pd.read_csv("katalog.csv")

try:
    df = lade_katalog()
    katalog_text = df.to_string(index=False)
except Exception as e:
    st.error(f"Katalog konnte nicht geladen werden: {e}")
    st.stop()

# --- 4. NUTZEREINGABE ---
problem_beschreibung = st.text_area(
    "Wo hakt es in Ihrem Projekt?", 
    placeholder="z.B. Ich benötige Hilfe bei der IFC-Strukturierung...", 
    height=150
)

# --- 5. KI-LOGIK ---
if st.button("Passende Lösung finden"):
    if problem_beschreibung:
        with st.spinner("Katalog wird durchsucht..."):
            system_prompt = f"""
            Du bist der fachliche Berater für BIM-Publikationen.
            Hier ist unser aktueller Katalog:
            {katalog_text}

            DEINE REGELN:
            1. Empfiehl NUR Bücher aus der obigen Liste. Erfinde nichts!
            2. Wenn das Problem nicht zu den Büchern passt, antworte freundlich, dass wir dazu aktuell keine Publikation führen.
            3. Antworte in 3-4 Sätzen. Nenne den Buchtitel in **Fett** und gib den Link an.

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