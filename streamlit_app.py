import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Pescador Pro", page_icon="🎣")

st.markdown("""
    <style>
    div.stButton > button {
        height: 70px;
        width: 100%;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 12px;
        background-color: #f8f9fa;
        border: 2px solid #007bff;
    }
    .net-card {
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
        background-color: #ffffff;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE CRITICAL FIX: INITIALIZE EVERYTHING FIRST ---
# This block MUST run before anything else to prevent NameErrors
if 'nets' not in st.session_state:
    st.session_state['nets'] = {"Net 1": 0.0, "Net 2": 0.0, "Net 3": 0.0, "Net 4": 0.0, "Net 5": 0.0}
if 'end_time' not in st.session_state:
    st.session_state['end_time'] = None
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- 3. HEADER & WEATHER ---
st.title("Pescador Pro 🎣")
col_header1, col_header2 = st.columns([2, 1])
with col_header1:
    venue = st.text_input("Venue / Lugar", placeholder="Rio Guadiana...")
with col_header2:
    st.info("☀️ 24°C\n💨 10km/h")

# --- 4. TIMER ---
st.subheader("Match Timer")
t_choice = st.radio("Duration", ["4h", "5h", "6h"], horizontal=True, label_visibility="collapsed")

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button("🚀 START"):
        st.session_state.end_time = datetime.now() + timedelta(hours=int(t_choice[0]))
with col_t2:
    if st.button("🛑 RESET"):
        st.session_state.end_time = None

timer_box = st.empty()

# --- 5. WEIGHTS & 5 NETS ---
st.divider()
st.subheader("Weight Logger")

# Active Net Selector
selected_net = st.radio("Active Net:", list(st.session_state.nets.keys()), horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1:
    if st.button("➕ 1.0 kg"):
        st.session_state.nets[selected_net] += 1.0
with col_w2:
    if st.button("➕ 0.5 kg"):
        st.session_state.nets[selected_net] += 0.5

# Visual Net Display
st.write("")
net_cols = st.columns(5)
for i, (name, val) in enumerate(st.session_state.nets.items()):
    status_color = "red" if val >= 18.0 else "#007bff" if val > 0 else "#6c757d"
    net_cols[i].markdown(f"""<div class='net-card'><strong>{name}</strong><br>
    <span style='color:{status_color}; font-weight:bold;'>{val:.1f}k</span></div>""", unsafe_allow_html=True)

total_all = sum(st.session_state.nets.values())
st.metric("TOTAL WEIGHT", f"{total_all:.2f} kg")

if st.button("🔄 Reset " + selected_net):
    st.session_state.nets[selected_net] = 0.0
    st.rerun()

# --- 6. NOTES & HISTORY ---
st.divider()
notes = st.text_area("Match Notes")
if st.button("💾 SAVE MATCH"):
    st.session_state.history.append({"date": datetime.now().strftime("%d/%m"), "v": venue, "w": total_all})
    st.success("Saved to History!")

# --- 7. TIMER REFRESH ---
if st.session_state.end_time:
    if st.session_state.end_time > datetime.now():
        diff = st.session_state.end_time - datetime.now()
        ts = int(diff.total_seconds())
        timer_box.header(f"⏳ {ts//3600:02d}:{(ts%3600)//60:02d}:{ts%60:02d}")
        time.sleep(1)
        st.rerun()
    else:
        timer_box.error("🏁 MATCH FINISHED")
