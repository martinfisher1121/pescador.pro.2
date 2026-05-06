import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLING (MAX BUTTON SIZE) ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

st.markdown("""
    <style>
    /* Super-Sized Weight Buttons */
    div.stButton > button:first-child {
        height: 120px !important;
        font-size: 40px !important;
        background-color: #007bff !important;
        color: white !important;
    }
    /* Half Kilo Button */
    div.stButton > button {
        height: 80px;
        font-size: 25px !important;
        font-weight: bold;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .net-card {
        padding: 5px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
        background-color: #ffffff;
        margin-bottom: 5px;
    }
    .history-card {
        padding: 10px;
        border-left: 5px solid #007bff;
        background-color: #f8f9fa;
        margin-bottom: 10px;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MULTI-LANGUAGE DICTIONARY ---
languages = {
    "English": {"venue": "Venue", "timer": "Match Timer", "start": "🚀 START", "reset": "🛑 RESET", "logger": "Weight Logger", "net": "Active Net", "total": "TOTAL", "save": "💾 SAVE MATCH", "press": "Pressure", "notes": "Tactical Notes", "history": "Match History"},
    "Español": {"venue": "Escenario", "timer": "Temporizador", "start": "🚀 INICIO", "reset": "🛑 RESET", "logger": "Contador", "net": "Rejón Activo", "total": "TOTAL", "save": "💾 GUARDAR", "press": "Presión", "notes": "Notas Tácticas", "history": "Historial de Encuentros"},
    "Français": {"venue": "Lieu", "timer": "Chrono", "start": "🚀 DEBUT", "reset": "🛑 RESET", "logger": "Poids", "net": "Bourriche", "total": "TOTAL", "save": "💾 SAUVER", "press": "Pression", "notes": "Notes Tactiques", "history": "Historique"},
    "Deutsch": {"venue": "Gewässer", "timer": "Timer", "start": "🚀 START", "reset": "🛑 RESET", "logger": "Gewicht", "net": "Setzkescher", "total": "GESAMT", "save": "💾 SPEICHERN", "press": "Druck", "notes": "Notizen", "history": "Verlauf"}
}

# --- 3. INITIALIZE STATE ---
if 'nets' not in st.session_state:
    st.session_state['nets'] = {"N1": 0.0, "N2": 0.0, "N3": 0.0, "N4": 0.0, "N5": 0.0}
if 'end_time' not in st.session_state:
    st.session_state['end_time'] = None
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- 4. HEADER: LANGUAGE & WEATHER ---
col_lang, col_wea = st.columns([1, 2])
with col_lang:
    sel_lang = st.selectbox("🌐", ["English", "Español", "Français", "Deutsch"], label_visibility="collapsed")
    text = languages[sel_lang]
with col_wea:
    st.info(f"☀️ 24°C | 💨 10km/h\n📉 {text['press']}: 1015hPa")

st.title("Pescador Pro 🎣")
venue_input = st.text_input(text['venue'], placeholder="e.g. Rio Guadiana")

# --- 5. TIMER ---
st.subheader(text['timer'])
t_choice = st.radio("Duration", ["4h", "5h", "6h"], horizontal=True, label_visibility="collapsed")

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button(text['start']):
        st.session_state.end_time = datetime.now() + timedelta(hours=int(t_choice[0]))
with col_t2:
    if st.button(text['reset']):
        st.session_state.end_time = None

timer_box = st.empty()

# --- 6. WEIGHTS & 5 NETS ---
st.divider()
st.subheader(text['logger'])
active_net = st.radio(text['net'], list(st.session_state.nets.keys()), horizontal=True)

# GIANT BUTTONS
if st.button("➕ 1.0 kg"):
    st.session_state.nets[active_net] += 1.0
if st.button("➕ 0.5 kg"):
    st.session_state.nets[active_net] += 0.5

# Visual 5-Net Status
st.write("")
net_cols = st.columns(5)
for i, (name, val) in enumerate(st.session_state.nets.items()):
    status_color = "red" if val >= 18.0 else "#007bff" if val > 0 else "#6c757d"
    net_cols[i].markdown(f"""<div class='net-card'><strong>{name}</strong><br>
    <span style='color:{status_color}; font-weight:bold; font-size:16px;'>{val:.1f}k</span></div>""", unsafe_allow_html=True)

total_all = sum(st.session_state.nets.values())
st.metric(text['total'], f"{total_all:.2f} kg")

# --- 7. NOTES & SAVE ---
st.divider()
notes_input = st.text_area(text['notes'], height=100)

if st.button(text['save']):
    save_data = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "v": venue_input if venue_input else "---",
        "w": f"{total_all:.2f} kg",
        "n": notes_input
    }
    st.session_state.history.append(save_data)
    st.success("✅ Saved!")

# --- 8. HISTORY DISPLAY ---
st.subheader(text['history'])
if not st.session_state.history:
    st.write("...")
else:
    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class='history-card'>
            <strong>📅 {item['timestamp']}</strong> | 📍 {item['v']}<br>
            <span style='font-size:18px;'>⚖️ {item['w']}</span><br>
            <small>📝 {item['n']}</small>
        </div>
        """, unsafe_allow_html=True)

# --- 9. TIMER REFRESH ---
if st.session_state.end_time:
    if st.session_state.end_time > datetime.now():
        diff = st.session_state.end_time - datetime.now()
        ts = int(diff.total_seconds())
        timer_box.header(f"⏳ {ts//3600:02d}:{(ts%3600)//60:02d}:{ts%60:02d}")
        time.sleep(1)
        st.rerun()
    else:
        timer_box.error("🏁 FINISHED")
