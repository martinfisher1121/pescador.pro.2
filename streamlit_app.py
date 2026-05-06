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
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE MEMORY (Session State) ---
if 'nets' not in st.session_state:
    st.session_state.nets = {"Net 1": 0.0, "Net 2": 0.0, "Net 3": 0.0, "Net 4": 0.0}
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. HEADER & VENUE ---
st.title("Pescador Pro 🎣")
venue = st.text_input("Venue / Lugar", placeholder="e.g. Rio Guadiana")

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

# --- 5. MULTI-NET WEIGHT LOGGER ---
st.divider()
st.subheader("Net Logger (18kg Limit)")

# Select which net to add weight to
active_net = st.radio("Active Net:", ["Net 1", "Net 2", "Net 3", "Net 4"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1:
    if st.button("➕ 1.0 kg"):
        st.session_state.nets[active_net] += 1.0
with col_w2:
    if st.button("➕ 0.5 kg"):
        st.session_state.nets[active_net] += 0.5

# Display current status of all nets
st.write("---")
n_cols = st.columns(4)
for i, name in enumerate(st.session_state.nets):
    w = st.session_state.nets[name]
    color = "red" if w >= 18.0 else "#007bff" if w > 0 else "gray"
    n_cols[i].markdown(f"<div class='net-box'><strong>{name}</strong><br><span style='color:{color}; font-size:20px;'>{w:.1f}kg</span></div>", unsafe_allow_html=True)

total_w = sum(st.session_state.nets.values())
st.metric("TOTAL MATCH WEIGHT", f"{total_w:.2f} kg")

if st.button("🔄 Clear Current Net"):
    st.session_state.nets[active_net] = 0.0
    st.rerun()

# --- 6. NOTES & SAVE ---
st.divider()
notes = st.text_area("Match Notes")

if st.button("💾 SAVE MATCH"):
    entry = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "venue": venue if venue else "Unknown",
        "weight": f"{total_w:.2f} kg"
    }
    st.session_state.history.append(entry)
    st.success("Saved!")

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
