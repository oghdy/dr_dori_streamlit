
import streamlit as st
import uuid
from openai import OpenAI
from supabase_client import supabase
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = "asst_YgT8jDSoCTNE82iwQlPlzn4w"

# ✅ 사용자 프로필로 새 Thread 생성
def create_new_thread_with_user_profile(user_info):
    user_context_message = f"""
User Profile:
- Age: {user_info['age']}
- Gender: {user_info['gender']}
- Pregnant: {'Yes' if user_info['pregnant'] else 'No'}
- Preferred Language: {user_info['language']}
"""
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_context_message
    )
    return thread.id

# ✅ 메시지를 Supabase에 저장
def save_message(user_email, thread_id, role, content):
    data = {
        "user_email": user_email,
        "thread_id": thread_id,
        "role": role,
        "content": content
    }
    supabase.table("chat_messages").insert(data).execute()

# ✅ 특정 Thread의 채팅 히스토리 불러오기
def display_chat_history(user_email, thread_id):
    response = supabase.table("chat_messages") \
        .select("*") \
        .eq("user_email", user_email) \
        .eq("thread_id", thread_id) \
        .order("timestamp", desc=False) \
        .execute()

    if response.data:
        for message in response.data:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("No previous conversations found.")

# ✅ Supabase에서 기존 Thread ID 가져오기
def get_existing_thread_id(user_email):
    response = supabase.table("chat_messages") \
        .select("thread_id") \
        .eq("user_email", user_email) \
        .order("timestamp", desc=True) \
        .limit(1) \
        .execute()

    if response.data and len(response.data) > 0:
        return response.data[0]["thread_id"]
    else:
        return None

# ✅ Assistant에게 질문 보내고 답변 받기
def ask_dori(thread_id, user_input):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    while True:
        run_status = client.beta.threads.runs.retrieve(run.id, thread_id=thread_id)
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0]
    return last_message.content[0].text.value

# ✅ Streamlit UI 메인 함수
def run_chat_interface(client, user_info=None):
    st.title("🦉 Chat with Dori")

    if "user_id" not in st.session_state:
        st.error("로그인이 필요합니다.")
        return

    # ✅ 로그인 후 첫 진입 시, thread_id 찾기
    if "thread_id" not in st.session_state:
        existing_thread_id = get_existing_thread_id(st.session_state["user_id"])
        if existing_thread_id:
            st.session_state["thread_id"] = existing_thread_id
        else:
            st.session_state["thread_id"] = create_new_thread_with_user_profile(user_info)

    display_chat_history(st.session_state["user_id"], st.session_state["thread_id"])

    # ✅ Quick Questions 추천 질문 버튼
    if "preset_input" not in st.session_state:
        st.session_state["preset_input"] = None

    if st.session_state["preset_input"] is None:
        st.markdown("### 📝 Quick Questions")
        q1, q2, q3 = st.columns(3)
        with q1:
            if st.button("I feel sick, help me Dori!"):
                st.session_state["preset_input"] = "I feel sick and need help. What should I do?"
                st.rerun()
        with q2:
            if st.button("Can I use my health insurance?"):
                st.session_state["preset_input"] = "Can I use my health insurance at Korean hospitals?"
                st.rerun()
        with q3:
            if st.button("How do I take this medicine?"):
                st.session_state["preset_input"] = "I got a prescription. How should I take this medicine?"
                st.rerun()

    # ✅ 기본 채팅 입력창
    user_input = st.chat_input("Ask Dori anything...")

    # 🔥 preset_input을 user_input처럼 사용
    if st.session_state["preset_input"]:
        user_input = st.session_state["preset_input"]
        st.session_state["preset_input"] = None

    # ✅ 질문 처리
    if user_input:
        with st.spinner("Dori is thinking..."):
            reply = ask_dori(st.session_state["thread_id"], user_input)

        save_message(st.session_state["user_id"], st.session_state["thread_id"], "user", user_input)
        save_message(st.session_state["user_id"], st.session_state["thread_id"], "assistant", reply)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="assets/dori_2D.png"):
            st.markdown(reply)

        st.rerun()





   


