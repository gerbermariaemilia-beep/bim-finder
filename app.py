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
    
    /* Buttons einheitliches Design */
    div.stButton > button {
        background-color: #032B5E !important;
        color: #FFFFFF !important; /* Button Textfarbe */
        border-radius: 5px;
        font-weight: bold;
        border: none;
        width: 100%;
        height: 50px;
        transition: 0.3s;
    }
    
    /* Button Hover Effekt */
    div.stButton > button:hover {
        background-color: #EC1616 !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIK ---
st.title("📚 BIM Publikations-Finder")
# ... (Katalog laden wie gehabt)

# --- BUTTONS NEU GEORDNET ---
col1, col2 = st.columns([3, 1]) # Jetzt ist die Suchen-Spalte größer (links)

with col1:
    suchen_btn = st.button("Passende Lösung finden")

with col2:
    loeschen_btn = st.button("Löschen")

# Logik für Buttons
if loeschen_btn:
    st.session_state.input_text = ""
    st.rerun()

if suchen_btn:
    # ... (Dein KI-Aufruf)
