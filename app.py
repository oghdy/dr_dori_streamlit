
import streamlit as st
from auth.login import login_page
from auth.signup import signup_page
from main_app import main_page

# ✅ 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# ✅ 로그인 안 되어있으면 로그인/회원가입 선택
if not st.session_state["logged_in"]:
    st.title("Welcome to Dr.dori! 🏥")

    menu = st.radio("Choose an option:", ("Login", "Sign Up"))

    if menu == "Login":
        login_page()
    else:
        signup_page()

# ✅ 로그인 성공했으면 메인화면으로 이동
else:
    main_page()


st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #E0F7FA; /* 민트색 */
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)








