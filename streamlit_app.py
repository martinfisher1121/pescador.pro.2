import streamlit as st

st.title("Pescador Pro 🎣")

# 1. Weather Section (New)
with st.expander("Current Weather Conditions"):
    st.write("Location: Detected (Spain)")
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("Temp", "22°C")
    col_w2.metric("Wind", "12 km/h NW")
    col_w3.metric("Pressure", "1015 hPa")

# 2. Match Timers (New)
st.subheader("Match Timer")
match_type = st.radio("Select Match Length:", ("4 Hours", "5 Hours"), horizontal=True)

# 3. Original Weight Style (Restored)
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

# Display the weight exactly like the old version
st.metric("Total Weight", f"{st.session_state.total_weight:.2f} kg")

# Net limit alert
if st.session_state.total_weight >= 18.0:
    st.error("⚠️ NET LIMIT NEAR! (20kg)")

if st.button("Reset Weight"):
    st.session_state.total_weight = 0.0
