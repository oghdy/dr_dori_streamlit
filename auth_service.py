
# auth_service.py
from supabase_client import supabase

# ✅ 회원가입 함수
def register_user(email, password):
    data = {"email": email, "password": password}
    try:
        response = supabase.table("users").insert(data).execute()
        if response.status_code == 201:
            return True, "회원가입 성공!"
        else:
            return False, response.data
    except Exception as e:
        return False, str(e)

# ✅ 로그인 함수
def login_user(email, password):
    try:
        response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
        if len(response.data) > 0:
            return True, response.data[0]  # 로그인 성공, 유저 정보 반환
        else:
            return False, "이메일 또는 비밀번호가 틀렸습니다."
    except Exception as e:
        return False, str(e)
    
from supabase_client import supabase

def authenticate_user(email, password):
    response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
    
    if response.data and len(response.data) > 0:
        return True
    else:
        return False

