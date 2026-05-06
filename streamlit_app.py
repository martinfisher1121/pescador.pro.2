import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLING (Bigger Buttons) ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

# Custom CSS to make the +1kg and +500g buttons large
st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        width: 100%;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LANGUAGE DICTIONARY ---
languages = {
    "English": {"title": "Pescador Pro 🎣", "venue": "Venue", "timer": "Match Timer", "start": "🚀 Start", "reset_t": "🛑 Reset", "finished": "🏁 FINISHED", "logger": "Weight", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ NET LIMIT!", "notes": "Notes", "reset_all": "Reset All"},
    "Español": {"title": "Pescador Pro 🎣", "venue": "Escenario", "timer": "Temporizador", "start": "🚀 Empezar", "reset_t": "🛑 Reiniciar", "finished": "🏁 FINAL", "logger": "Pesaje", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ ¡REJÓN LLENO!", "notes": "Notas", "reset_all": "Borrar Todo"},
    "Français": {"title": "Pescador Pro 🎣", "venue": "Lieu", "timer": "Chrono", "start": "🚀 Démarrer", "reset_t": "🛑 Reset", "finished": "🏁 FINI", "logger": "Poids", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ BOURRICHE!", "notes": "Notes", "reset_all": "Tout Reset"},
    "Deutsch": {"title": "Pescador Pro 🎣", "venue": "Gewässer", "timer": "Timer", "start": "🚀 Start", "reset_t": "🛑 Reset", "finished": "🏁 ENDE", "logger": "Gewicht", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Gesamt", "limit": "⚠️ KESCHER!", "notes": "Notizen", "reset_all": "Reset"}
}

sel_lang = st.selectbox("🌐 Language", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]

st.title(text["title"])

# --- 3. VENUE & TIMER ---
venue = st.text_input(text["venue"], placeholder="...")

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

# --- LIVE COUNTDOWN DISPLAY ---
timer_placeholder = st.empty()

# --- 4. CATCH LOGGER (Bigger Buttons) ---
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

if st.session_state.total_weight >= 18.0:
    st.error(text["limit"])

# --- 5. NOTES & RESET ---
match_notes = st.text_area(text["notes"])

if st.button(text["reset_all"]):
    st.session_state.total_weight = 0.0
    st.session_state.end_time = None
    st.rerun()

# --- 6. CONTINUOUS TIMER LOGIC ---
while st.session_state.end_time is not None:
    remaining = st.session_state.end_time - datetime.now()
    if remaining.total_seconds() > 0:
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        timer_placeholder.header(f"⏳ {hrs:02d}:{mins:02d}:{secs:02d}")
        time.sleep(1)
        st.rerun() # This forces the app to refresh every second
    else:
        timer_placeholder.error(text["finished"])
        st.session_state.end_time = None
        break
