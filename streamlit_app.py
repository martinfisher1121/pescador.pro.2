import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

# --- 1. LANGUAGE DICTIONARY ---
languages = {
    "English": {
        "title": "Pescador Pro 🎣",
        "venue": "Venue Name",
        "weather": "Local Weather",
        "timer": "Match Timer",
        "duration": "Select Duration",
        "start": "🚀 Start Match",
        "reset_t": "🛑 Reset Timer",
        "finished": "🏁 MATCH FINISHED!",
        "logger": "Catch Logger",
        "add1": "➕ Add 1kg",
        "add500": "➕ Add 500g",
        "weight": "Total Weight",
        "limit": "⚠️ NET LIMIT NEAR!",
        "notes": "Match Notes",
        "reset_all": "Reset All Data",
        "placeholder_v": "e.g., Rio Guadiana",
        "placeholder_n": "Tactics, bait, wind..."
    },
    "Español": {
        "title": "Pescador Pro 🎣",
        "venue": "Nombre del Escenario",
        "weather": "Clima Local",
        "timer": "Temporizador de Competición",
        "duration": "Seleccionar Duración",
        "start": "🚀 Empezar",
        "reset_t": "🛑 Reiniciar Reloj",
        "finished": "🏁 ¡FINAL DEL CONCURSO!",
        "logger": "Registro de Capturas",
        "add1": "➕ Añadir 1kg",
        "add500": "➕ Añadir 500g",
        "weight": "Peso Total",
        "limit": "⚠️ ¡LÍMITE DE REJÓN CERCA!",
        "notes": "Notas del Concurso",
        "reset_all": "Borrar Todo",
        "placeholder_v": "ej. Río Guadiana",
        "placeholder_n": "Tácticas, cebo, viento..."
    },
    "Français": {
        "title": "Pescador Pro 🎣",
        "venue": "Nom du Lieu",
        "weather": "Météo Locale",
        "timer": "Chronomètre de Match",
        "duration": "Choisir la Durée",
        "start": "🚀 Démarrer",
        "reset_t": "🛑 Reset Chrono",
        "finished": "🏁 MATCH TERMINÉ!",
        "logger": "Registre des Prises",
        "add1": "➕ Ajouter 1kg",
        "add500": "➕ Ajouter 500g",
        "weight": "Poids Total",
        "limit": "⚠️ LIMITE DE BOURRICHE PROCHE!",
        "notes": "Notes de Match",
        "reset_all": "Tout Réinitialiser",
        "placeholder_v": "ex. Rivière Guadiana",
        "placeholder_n": "Tactiques, appâts, vent..."
    },
    "Deutsch": {
        "title": "Pescador Pro 🎣",
        "venue": "Gewässername",
        "weather": "Lokales Wetter",
        "timer": "Match-Timer",
        "duration": "Dauer Wählen",
        "start": "🚀 Starten",
        "reset_t": "🛑 Timer Zurücksetzen",
        "finished": "🏁 ANGELN BEENDET!",
        "logger": "Fangbuch",
        "add1": "➕ 1kg Hinzufügen",
        "add500": "➕ 500g Hinzufügen",
        "weight": "Gesamtgewicht",
        "limit": "⚠️ KESCHERGRENZE NAHE!",
        "notes": "Notizen",
        "reset_all": "Alles Zurücksetzen",
        "placeholder_v": "z.B. Guadiana Fluss",
        "placeholder_n": "Taktik, Köder, Wind..."
    }
}

# --- 2. LANGUAGE SELECTOR ---
sel_lang = st.selectbox("🌐 Language / Idioma", ["English", "Español", "Français", "Deutsch"])
text = languages[sel_lang]

st.title(text["title"])

# --- 3. VENUE & WEATHER ---
st.subheader(text["venue"])
venue = st.text_input(text["venue"], label_visibility="collapsed", placeholder=text["placeholder_v"])

with st.expander(text["weather"]):
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("Temp", "22°C")
    col_w2.metric("Wind", "12km/h NW")
    col_w3.metric("Pressure", "1015 hPa")

# --- 4. COUNTDOWN TIMER ---
st.subheader(text["timer"])
match_length = st.radio(text["duration"], ["4 Hours", "5 Hours"], horizontal=True)

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

if st.session_state.end_time:
    remaining = st.session_state.end_time - datetime.now()
    if remaining.total_seconds() > 0:
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        st.header(f"⏳ {hrs:02d}:{mins:02d}:{secs:02d}")
    else:
        st.error(text["finished"])

# --- 5. CATCH LOGGER ---
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
    st.warning(text["limit"])

# --- 6. NOTES ---
st.subheader(text["notes"])
match_notes = st.text_area("Notes", label_visibility="collapsed", placeholder=text["placeholder_n"])

if st.button(text["reset_all"]):
    st.session_state.total_weight = 0.0
    st.session_state.end_time = None
    st.rerun()
