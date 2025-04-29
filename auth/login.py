
import streamlit as st
from supabase_client import supabase

def login_page():
    st.title("login 🔑")

    email = st.text_input("email", placeholder="example@email.com")
    password = st.text_input("password", type="password", placeholder="enter password")

    if st.button("login"):
        if not email or not password:
            st.error("Please enter both email and password")
            return

        # Supabase에서 이메일, 비밀번호 일치하는지 확인
        response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()

        if response.data:
            st.success("Login successful!!🎯")
            st.session_state["user_id"] = email
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Email or password is incorrect.")