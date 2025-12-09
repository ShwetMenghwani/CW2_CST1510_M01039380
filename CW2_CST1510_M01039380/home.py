import streamlit as st
from app.services.user_service import login_user

# --- Page configuration ---
st.set_page_config(page_title="Intelligence Platform Login", layout="centered")

# --- Session state initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "page_reload_needed" not in st.session_state:
    st.session_state.page_reload_needed = False

# --- Page title ---
st.title("Login")

# ------------------------
# LOGIN FORM
# ------------------------
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, msg, role = login_user(username, password)  # Get role too
        st.info(msg)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role  # store role in session

# ------------------------
# AFTER LOGIN
# ------------------------
if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username}!")

    # Show role-based dashboard buttons
    if st.session_state.role == "cyber":
        st.write("You can access Cybersecurity Dashboard")
    elif st.session_state.role == "datasci":
        st.write("You can access Data Science Dashboard")
    elif st.session_state.role == "itops":
        st.write("You can access IT Operations Dashboard")
    else:
        st.write("Role not recognized")
    # ------------------------
    # LOGOUT BUTTON
    # ------------------------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
