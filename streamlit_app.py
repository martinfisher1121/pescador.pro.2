import streamlit as st
import time
from datetime import datetime, timedelta

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
    .history-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MULTI-LANGUAGE DICTIONARY ---
languages = {
    "English": {"title": "Pescador Pro 🎣", "venue": "Venue", "weather": "Weather", "timer": "Match Timer", "start": "🚀 START", "reset_t": "🛑 RESET", "finished": "🏁 FINISHED", "logger": "Weight Logger", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ NET LIMIT!", "notes": "Match Notes", "save": "💾 SAVE MATCH", "history": "History"},
    "Español": {"title": "Pescador Pro 🎣", "venue": "Escenario", "weather": "Clima", "timer": "Temporizador", "start": "🚀 EMPEZAR", "reset_t": "🛑 REINICIAR", "finished": "🏁 FINAL", "logger": "Contador de Peso", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ ¡REJÓN LLENO!", "notes": "Notas", "save": "💾 GUARDAR", "history": "Historial"},
    "Français": {"title": "Pescador Pro 🎣", "venue": "Lieu", "weather": "Météo", "timer": "Chrono", "start": "🚀 DÉMARRER", "reset_t": "🛑 RESET", "finished": "🏁 FINI", "logger": "Poids", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Total", "limit": "⚠️ BOURRICHE!", "notes": "Notes", "save": "💾 SAUVER", "history": "Historique"},
    "Deutsch": {"title": "Pescador Pro 🎣", "venue": "Gewässer", "weather": "Wetter", "timer": "Timer", "start": "🚀 START", "reset_t": "🛑 RESET", "finished": "🏁 ENDE", "logger": "Gewicht", "add1": "➕ 1kg", "add500": "➕ 500g", "weight": "Gesamt", "limit": "⚠️ KESCHER!", "notes": "Notizen", "save": "💾 SPEICHERN", "history": "Historie"}
}

# --- 3. STATE & SELECTIONS ---
sel_lang = st.selectbox("🌐 Language", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]

if 'total_weight' not in st.session_state: st.session_state.total_weight = 0.0
if 'end_time' not in st.session_state: st.session_state.end_time = None
if 'history' not in st.session_state: st.session_state.history = []

st.title(text["title"])

# --- 4. VENUE & WEATHER ---
venue_name = st.text_input(text["venue"], placeholder="e.g. Rio Guadiana")
with st.expander(text["weather"], expanded=True):
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("Temp", "22°C")
    col_w2.metric("Wind", "12km/h NW")
    col_w3.metric("Baro", "1015 hPa")

# --- 5. THE LIVE TIMER ---
st.subheader(text["timer"])
match_length = st.radio("Duration", ["4h", "5h"], horizontal=True)

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button(text["start"]):
        hrs = 4 if "4" in match_length else 5
        st.session_state.end_time = datetime.now() + timedelta(hours=hrs)
with col_t2:
    if st.button(text["reset_t"]):
        st.session_state.end_time = None

timer_placeholder = st.empty()

# --- 6. THE WEIGHT LOG (GIANT BUTTONS) ---
st.subheader(text["logger"])
col1, col2 = st.columns(2)
with col1:
    if st.button(text["add1"]): st.session_state.total_weight += 1.0
with col2:
    if st.button(text["add500"]): st.session_state.total_weight += 0.5

st.metric(text["weight"], f"{st.session_state.total_weight:.2f} kg")

if st.session_state.total_weight >= 18.0:
    st.error(text["limit"])

# --- 7. NOTES & SAVE ---
notes = st.text_area(text["notes"])

if st.button(text["save"]):
    log_entry = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "venue": venue_name if venue_name else "---",
        "weight": f"{st.session_state.total_weight:.2f} kg"
    }
    st.session_state.history.append(log_entry)
    st.success("Match Saved!")

# --- 8. HISTORY DISPLAY ---
if st.session_state.history:
    st.divider()
    st.subheader(text["history"])
    for item in reversed(st.session_state.history):
        st.markdown(f"""<div class="history-box">📅 {item['date']} | 📍 {item['venue']} | ⚖️ <strong>{item['weight']}</strong></div>""", unsafe_allow_html=True)

# --- 9. LIVE COUNTDOWN LOGIC ---
if st.session_state.end_time:
    while st.session_state.end_time > datetime.now():
        rem = st.session_state.end_time - datetime.now()
        m, s = divmod(int(rem.total_seconds()), 60)
        h, m = divmod(m, 60)
        timer_placeholder.header(f"⏳ {h:02d}:{m:02d}:{s:02d}")
        time.sleep(1)
        st.rerun()
    timer_placeholder.error(text["finished"])
