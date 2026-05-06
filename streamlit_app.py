# --- 1. STATE FOR MULTIPLE NETS ---
if 'active_net' not in st.session_state: st.session_state.active_net = "Net 1"
if 'nets' not in st.session_state: 
    st.session_state.nets = {"Net 1": 0.0, "Net 2": 0.0, "Net 3": 0.0, "Net 4": 0.0}

# --- 2. NET SELECTOR (Tabs or Radio) ---
st.subheader("Select Active Net")
net_choice = st.radio("Which net are you filling?", ["Net 1", "Net 2", "Net 3", "Net 4"], horizontal=True)
st.session_state.active_net = net_choice

# --- 3. WEIGHT BUTTONS (Targets the selected net) ---
col_lb1, col_lb2 = st.columns(2)
with col_lb1:
    if st.button("➕ 1kg"): 
        st.session_state.nets[st.session_state.active_net] += 1.0
with col_lb2:
    if st.button("➕ 500g"): 
        st.session_state.nets[st.session_state.active_net] += 0.5

# --- 4. DISPLAY INDIVIDUAL NET WEIGHTS ---
st.markdown("---")
cols = st.columns(4)
for i, name in enumerate(st.session_state.nets):
    weight = st.session_state.nets[name]
    # Warning color if close to 18kg
    color = "red" if weight >= 18.0 else "green" if weight > 0 else "gray"
    cols[i].markdown(f"**{name}**\n<h3 style='color:{color};'>{weight:.1f}kg</h3>", unsafe_allow_html=True)

# --- 5. TOTAL WEIGHT & RESET ---
total = sum(st.session_state.nets.values())
st.metric("Total Weight (All Nets)", f"{total:.2f} kg")

if st.button("🔄 Reset Current Net", type="secondary"):
    st.session_state.nets[st.session_state.active_net] = 0.0
    st.rerun()
