import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Pescador Pro", page_icon="🎣")
st.title("Pescador Pro 🎣")

# --- 1. VENUE & WEATHER ---
st.subheader("Match Details")
venue = st.text_input("Venue Name", placeholder="e.g., Rio Guadiana")

with st.expander("Local Weather"):
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("Temp", "22°C")
    col_w2.metric("Wind", "12km/h NW")
    col_w3.metric("Pressure", "1015 hPa")

# --- 2. COUNTDOWN TIMER ---
st.subheader("Match Timer")
match_length = st.radio("Select Duration", ["4 Hours", "5 Hours"], horizontal=True)

if 'end_time' not in st.session_state:
    st.session_state.end_time = None

col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button("🚀 Start Match"):
        hours = 4 if match_length == "4 Hours" else 5
        st.session_state.end_time = datetime.now() + timedelta(hours=hours)

with col_t2:
    if st.button("🛑 Reset Timer"):
        st.session_state.end_time = None

# Logic to display the countdown
if st.session_state.end_time:
    remaining = st.session_state.end_time - datetime.now()
    if remaining.total_seconds() > 0:
        # Formats the time into H:M:S
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        st.header(f"⏳ {hrs:02d}:{mins:02d}:{secs:02d}")
    else:
        st.error("🏁 MATCH FINISHED!")

# --- 3. CATCH LOGGER (Original Style) ---
st.subheader("Catch Logger")
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 0.0

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add 1kg"):
        st.session_state.total_weight += 1.0
with col2:
    if st.button("➕ Add 500g"):
        st.session_state.total_weight += 0.5

st.metric("Total Weight", f"{st.session_state.total_weight:.2f} kg")

if st.session_state.total_weight >= 18.0:
    st.warning("⚠️ NET LIMIT NEAR!")

# --- 4. NOTES SECTION ---
st.subheader("Match Notes")
match_notes = st.text_area("Notes", placeholder="e.g., Fish feeding at 13m on corn, wind picking up...")

if st.button("Reset All Data"):
    st.session_state.total_weight = 0.0
    st.session_state.end_time = None
    st.rerun()
