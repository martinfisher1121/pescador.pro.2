import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. PAGE CONFIG & STYLE ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        width: 100%;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 15px;
        background-color: #f0f2f6;
        border: 2px solid #007bff;
    }
    .net-box {
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #ddd;
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE MEMORY ---
if 'nets' not in st.session_state:
    st.session_state.nets = {"Net 1": 0.0, "Net 2": 0.0, "Net 3": 0.0, "Net 4": 0.0, "Net 5": 0.0}
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. HEADER & WEATHER (The Weapon) ---
st.title("Pescador Pro 🎣")

col_v1, col_v2 = st.columns([2, 1])
with col_v1:
    venue = st.text_input("Venue / Lugar", placeholder="e.g. Rio Guadiana")
with col_v2:
    st.write("**Live Weather**")
    st.caption("☀️ 24°C | 💨 10km/h")

# --- 4. TIMER SECTION ---
st.subheader("Match Timer")
m_length = st.radio("Duration", ["4h", "5h", "6h"], horizontal=True)

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button("🚀 START"):
        hrs = int(m_length[0])
        st.session_state.end_time = datetime.now() + timedelta(hours=hrs)
with col_t2:
    if st.button("🛑 RESET TIMER"):
        st.session_state.end_time = None

timer_place = st.empty()

# --- 5. FIVE-NET WEIGHT LOGGER ---
st.divider()
st.subheader("Net Logger (18kg Limit)")

# Select which net to add weight to (Now includes Net 5)
active_net = st.radio("Select Net:", ["Net 1", "Net 2", "Net 3", "Net 4", "Net 5"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1:
    if st.button("➕ 1.0 kg"):
        st.session_state.nets[active_net] += 1.0
with col_w2:
    if st.button("➕ 0.5 kg"):
        st.session_state.nets[active_net] += 0.5

# Display current status of all 5 nets
st.write("---")
n_cols = st.columns(5)
for i, name in enumerate(st.session_state.nets):
    w = st.session_state.nets[name]
    # Warning color at 18kg
    color = "#d9534f" if w >= 18.0 else "#0275d8" if w > 0 else "#6c757d"
    n_cols[i].markdown(f"<div class='net-box'><strong>{name}</strong><br><span style='color:{color}; font-size:18px; font-weight:bold;'>{w:.1f}kg</span></div>", unsafe_allow_html=True)

total_w = sum(st.session_state.nets.values())
st.metric("TOTAL MATCH WEIGHT", f"{total_w:.2f} kg")

if st.button("🔄 Clear Active Net", type="secondary"):
    st.session_state.nets[active_net] = 0.0
    st.rerun()

# --- 6. NOTES & HISTORY ---
st.divider()
notes = st.text_area("Match Notes / Tactics")

if st.button("💾 SAVE MATCH"):
    entry = {"date": datetime.now().strftime("%d/%m/%Y"), "venue": venue, "weight": f"{total_w:.2f} kg"}
    st.session_state.history.append(entry)
    st.success("Match Saved!")

# --- 7. LIVE TIMER LOGIC ---
if st.session_state.end_time:
    rem = st.session_state.end_time - datetime.now()
    if rem.total_seconds() > 0:
        m, s = divmod(int(rem.total_seconds()), 60)
        h, m = divmod(m, 60)
        timer_place.header(f"⏳ {h:02d}:{m:02d}:{s:02d}")
        time.sleep(1)
        st.rerun()
    else:
        timer_place.error("🏁 FINISHED")
