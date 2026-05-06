import streamlit as st
import time
from datetime import datetime, timedelta
# Import the microphone component
from streamlit_mic_recorder import mic_recorder, speech_to_text

# --- 1. STYLING (The Giant Buttons) ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

st.markdown("""
    <style>
    div.stButton > button {
        height: 90px;
        width: 100%;
        font-size: 28px !important;
        font-weight: bold;
        border-radius: 20px;
        background-color: #f0f2f6;
        border: 2px solid #007bff;
    }
    .stTextArea textarea {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LANGUAGE DICTIONARY (Updated with Voice) ---
languages = {
    "English": {"notes": "Match Notes", "mic": "🎤 Tap to speak notes", "save": "💾 SAVE MATCH"},
    "Español": {"notes": "Notas del Encuentro", "mic": "🎤 Pulsa para hablar", "save": "💾 GUARDAR"},
    "Français": {"notes": "Notes de Match", "mic": "🎤 Appuyez pour parler", "save": "💾 SAUVER"},
    "Deutsch": {"notes": "Match-Notizen", "mic": "🎤 Zum Sprechen tippen", "save": "💾 SPEICHERN"}
}

sel_lang = st.selectbox("🌐 Language", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]

# --- 3. STATE MANAGEMENT ---
if 'note_text' not in st.session_state:
    st.session_state.note_text = ""

# ... (Insert the rest of the app logic: Weather, Timer, Weights here) ...

# --- 4. THE VOICE NOTES SECTION ---
st.subheader(text["notes"])

# This component creates the microphone button and processes the audio
spoken_text = speech_to_text(
    language='en' if sel_lang == "English" else 'es' if sel_lang == "Español" else 'fr' if sel_lang == "Français" else 'de',
    start_prompt=text["mic"],
    key='speech'
)

# If the user spoke, add it to our session state
if spoken_text:
    st.session_state.note_text += f" {spoken_text}"

# Display the notes in a text area so they can still edit if needed
notes = st.text_area("Final Notes", value=st.session_state.note_text, height=150, label_visibility="collapsed")

# Update state if they type manually
st.session_state.note_text = notes

if st.button(text["save"]):
    # Save logic as before...
    st.success("Match Saved with Voice Notes!")
