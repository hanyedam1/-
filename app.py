import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="모닝알람 챗봇 ☀️", page_icon="⏰", layout="centered")
st.title("⏰ 모닝알람 AI 챗봇")
st.subheader("당신의 활기찬 아침을 깨우는 AI 비서입니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
try:
    # Streamlit Cloud 배포 시 Secrets에 등록한 키를 가져옵니다.
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_api_key)
except KeyError:
    st.error("❌ Streamlit Secrets에서 'GEMINI_API_KEY'를 찾을 수 없습니다. 설정 확인이 필요합니다.")
    st.stop()

# 3. 세션 상태(Session State)로 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! ☀️ 기분 좋은 아침입니다. 오늘 아침 알람 소리는 잘 들으셨나요? 상쾌한 하루를 시작할 수 있도록 도와드릴게요. 오늘 날씨, 다짐, 혹은 잠을 깨기 위한 가벼운 퀴즈 중 무엇을 도와드릴까요?"
        }
    ]

# 4. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("메시지를 입력하세요... (예: 잠 깨는 퀴즈 내줘!)"):
    
    # 사용자 메시지 화면 표시 및 세션 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. AI 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔄 생각 중...")
        
        try:
            # gemini-2.5-flash-lite 모델 설정
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction="당신은 사용자의 아침을 깨워주는 다정하고 활기찬 '모닝알람 비서'입니다. 말투는 항상 긍정적이고 에너지가 넘쳐야 하며, 사용자가 잠에서 완전히 깨어날 수 있도록 유익한 대화를 유도하세요. 필요하다면 간단한 넌센스 퀴즈나 아침 스트레칭을 제안해도 좋습니다."
            )
            
            # 대화 기록 형식 변환 (Gemini API 양식에 맞춤)
            chat_history = []
            for msg in st.session_state.messages[:-1]:  # 방금 넣은 유저 입력 제외한 이전 기록
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            # 멀티턴 대화 시작
            chat = model.start_chat(history=chat_history)
            
            # 답변 요청
            response = chat.send_message(user_input)
            ai_response = response.text
            
            # 화면 업데이트 및 세션 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            # API 오류나 네트워크 오류 처리
            error_msg = f"⚠️ 답변을 생성하는 중에 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
