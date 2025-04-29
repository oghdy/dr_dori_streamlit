
import streamlit as st
from supabase_client import supabase
import time

def signup_page():
    st.title("Sign Up 📝")

    email = st.text_input("Email", placeholder="example@email.com")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Sign Up"):
        if not email or not password:
            st.error("Please fill in all fields")
            return

        # 이메일 중복 확인
        response = supabase.table("users").select("*").eq("email", email).execute()

        if response.data:
            st.error("This email is already registered.")
            return

        # 회원가입 진행
        new_user = {
            "email": email,
            "password": password
        }
        supabase.table("users").insert(new_user).execute()

        st.success("🎉 You've successfully signed up! Redirecting to the login page...")

        
        time.sleep(1)

        st.session_state["page"] = "login"
        st.rerun()
