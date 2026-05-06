import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLING (Bigger Buttons) ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

# Custom CSS to make the weight buttons and action buttons large and easy to hit
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
    </style>
""", unsafe_allow_html=True)

# --- 2. LANGUAGE DICTIONARY ---
languages = {
    "English": {"title": "Pescador Pro 🎣", "venue": "Venue", "weather": "Local Weather", "timer": "Match Timer", "start": "🚀 Start", "reset_t": "🛑 Reset", "finished": "🏁 FINISHED", "logger": "Weight", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ NET LIMIT!", "notes": "Notes", "reset_all": "Reset All Data"},
    "Español": {"title": "Pescador Pro 🎣", "venue": "Escenario", "weather": "Clima Local", "timer": "Temporizador", "start": "🚀 Empezar", "reset_t": "🛑 Reiniciar", "finished": "🏁 FINAL", "logger": "Pesaje", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ ¡REJÓN LLENO!", "notes": "Notas", "reset_all": "Borrar Todo"},
    "Français": {"title": "Pescador Pro 🎣", "venue": "Lieu", "weather": "Météo Locale", "timer": "Chrono", "start": "🚀 Démarrer", "reset_t": "🛑 Reset", "finished": "🏁 FINI", "logger": "Poids", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ BOURRICHE!", "notes": "Notes", "reset_all": "Tout Reset"},
    "Deutsch": {"title": "Pescador Pro 🎣", "venue": "Gewässer", "weather": "Lokales Wetter", "timer": "Timer", "start": "🚀 Start", "reset_t": "🛑 Reset", "finished": "🏁 ENDE", "logger": "Gewicht", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Gesamt", "limit": "⚠️ KESCHER!", "notes": "Notizen", "reset_all": "Alles Zurücksetzen"}
}

# Language Selection
sel_lang = st.selectbox("🌐 Language / Idioma", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]

st.title(text["title"])

# --- 3. VENUE & WEATHER (Restored) ---
st.subheader(text["venue"])
venue = st.text_input(text["venue"], label_visibility="collapsed", placeholder="...")

with st.expander(text["weather"], expanded=True):
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("Temp", "22°C")
    col_w2.metric("Wind", "12km/h NW")
    col_w3.metric("Pressure", "1015 hPa")

# --- 4. LIVE MATCH TIMER ---
st.subheader(text["timer"])
match_length = st.radio("Duration", ["4h", "5h"], horizontal=True)

if 'end_time' not in st.session_state:
    st.session_state.end_time = None

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button(text["start"]):
        hours = 4 if "4" in match_length else 5
        st.session_state.end_time = datetime.now() + timedelta(hours=hours)
with col_t2:
    if st.button(text["reset_t"]):
        st.session_state.end_time = None

# Placeholder for the ticking clock
timer_placeholder = st.empty()

# --- 5. CATCH LOGGER (Giant Buttons) ---
st.subheader(text["logger"])
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0.0

col1, col2 = st.columns(2)
with col1:
    if st.button(text["add1"]):
        st.session_state.total_weight += 1.0
with col2:
    if st.button(text["add500"]):
        st.session_state.total_weight += 0.5

st.metric(text["weight"], f"{st.session_state.total_weight:.2f} kg")

# Net limit warning
if st.session_state.total_weight >= 18.0:
    st.error(text["limit"])

# --- 6. NOTES & MASTER RESET ---
st.subheader(text["notes"])
match_notes = st.text_area(text["notes"], label_visibility="collapsed")

if st.button(text["reset_all"]):
    st.session_state.total_weight = 0.0
    st.session_state.end_time = None
    st.rerun()

# --- 7. CONTINUOUS TIMER LOGIC ---
# This loop keeps the app refreshing every second while the match is active
while st.session_state.end_time is not None:
    remaining = st.session_state.end_time - datetime.now()
    if remaining.total_seconds() > 0:
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        timer_placeholder.header(f"⏳ {hrs:02d}:{mins:02d}:{secs:02d}")
        time.sleep(1)
        st.rerun() 
    else:
        timer_placeholder.error(text["finished"])
        st.session_state.end_time = None
        break
