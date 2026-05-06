import streamlit as st
import time

st.title("Pescador Pro 🎣")

# 1. Weather Section
with st.expander("Current Weather Conditions"):
    st.write("Location: Detected (Spain)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temp", "22°C")
    col2.metric("Wind", "12 km/h NW")
    col3.metric("Pressure", "1015 hPa")

# 2. Match Timer Selection
st.subheader("Match Timer")
match_type = st.radio("Select Match Length:", ("4 Hours", "5 Hours"), horizontal=True)

if st.button("Start Match"):
    duration = 4 if match_type == "4 Hours" else 5
    st.success(f"{duration} Hour Match Started!")
    # Timer logic runs here

# 3. Catch & Net Management
st.subheader("Catch Logger")
current_weight = st.number_input("Current Total Weight (kg)", min_value=0.0, step=0.1)

if current_weight >= 18.0:
    st.warning("⚠️ Approaching Net Limit (20kg)! Prepare second net.")
