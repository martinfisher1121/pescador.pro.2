import streamlit as st

# --- ACCESS CONTROL ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Pescador Pro 🎣")
    st.write("### 🇪🇸 ¡Hola, pescador!")
    st.write("Subscribe to unlock the full match dashboard (Timers, Weight Logger, and Memory).")
    
    # In a real setup, this button would trigger the Bizum / Redsys payment
    if st.button("🚀 Unlock for €2.00 (Bizum / Card)"):
        # This is a placeholder for the bank transaction
        st.session_state.authenticated = True
        st.rerun()
    
    st.stop() # This stops the rest of the app from loading until paid

# --- THE REST OF YOUR APP CODE GOES BELOW HERE ---
st.success("Access Granted! Tight lines.")
