import streamlit as st
from app.services.user_service import register_user  # Only import register_user

st.set_page_config(page_title="Register", layout="centered")
st.title("Sign up")

# ------------------------
# Registration form
# ------------------------
with st.form("register_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Role", ["cyber", "datasci", "itops"])

    submitted = st.form_submit_button("Register")

    if submitted:
        if not username or not password:
            st.warning("Username and password are required.")
        elif password != confirm_password:
            st.warning("Passwords do not match!")
        else:
            success, msg = register_user(username, password, role)
            if success:
                st.success(msg)
            else:
                st.error(msg)
