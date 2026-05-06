import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. STYLING & CONFIG ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

st.markdown("""
    <style>
    div.stButton > button {
        height: 85px;
        width: 100%;
        font-size: 26px !important;
        font-weight: bold;
        border-radius: 15px;
        background-color: #f0f2f6;
    }
    .history-box {
        padding: 10px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LANGUAGE DICTIONARY ---
languages = {
    "English": {"save": "💾 Save to History", "history": "Match History", "date": "Date"},
    "Español": {"save": "💾 Guardar Historial", "history": "Historial de Pesca", "date": "Fecha"},
    "Français": {"save": "💾 Enregistrer", "history": "Historique", "date": "Date"},
    "Deutsch": {"save": "💾 Speichern", "history": "Fanghistorie", "date": "Datum"}
}

# (Existing Dictionary content merged for brevity)
sel_lang = st.selectbox("🌐 Language", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]
# Note: Add the rest of the labels from previous code here...

# --- 3. SESSION STATE INITIALIZATION ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0.0
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

# --- 4. APP INTERFACE (Venue, Weather, Timer, Weight - as before) ---
st.title("Pescador Pro 🎣")
venue = st.text_input("Venue", placeholder="...")

# --- 5. THE SAVE BUTTON ---
if st.button(text["save"]):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "venue": venue if venue else "Unknown",
        "weight": f"{st.session_state.total_weight:.2f} kg",
        "weather": "22°C, 12km/h NW", # This can be made dynamic later
        "notes": "See Match Notes" 
    }
    st.session_state.history.append(entry)
    st.success("Data Saved!")

# --- 6. MATCH HISTORY DISPLAY ---
st.divider()
st.subheader(text["history"])

for item in reversed(st.session_state.history):
    with st.container():
        st.markdown(f"""
        <div class="history-box">
            <strong>📅 {text['date']}:</strong> {item['date']} | <strong>📍 {item['venue']}</strong><br>
            <strong>⚖️ {item['weight']}</strong> | 🌤️ {item['weather']}
        </div>
        """, unsafe_allow_html=True)
