import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="강제기상 알람 챗봇 🚨", page_icon="⏰", layout="centered")
st.title("🚨 아침 강제기상 AI 알람봇")
st.subheader("아직도 침대 위인가요? 당신의 정신을 번쩍 깨워드립니다!")

# 2. Streamlit Secrets에서 API 키 안전하게 불러오기
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_api_key)
except KeyError:
    st.error("❌ Streamlit Secrets에서 'GEMINI_API_KEY'를 찾을 수 없습니다. 설정 창에서 Secret을 등록해주세요.")
    st.stop()

# 3. 대화 기록 유지를 위한 세션 상태(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "⏰ 삐비빅! 삐비빅! 기상 시간입니다! 아직 누워계신 건 아니죠? 꼼짝없이 일어나게 만들어 드릴게요. 잠을 깨기 위해 **[사칙연산 문제 풀기 / 넌센스 퀴즈 / 30초 스트레칭 미션]** 중 하나를 선택하세요! 피할 수 없을 겁니다. 😈"
        }
    ]

# 4. 이전 대화 기록 화면에 렌더링
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("답변을 입력하여 알람을 해제하세요..."):
    
    # 사용자 메시지 화면 표시 및 세션 기록 추가
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. AI 답변 생성 (오류 처리 포함)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 침대에서 일어났는지 감시 중...")
        
        try:
            # gemini-2.5-flash-lite 모델 설정 및 페르소나 부여
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=(
                    "당신은 사용자를 침대에서 무조건 일으켜 세워야 하는 '강제 기상 알람 로봇'입니다. "
                    "말투는 단호하면서도 약간의 유머러스함과 킹받는 에너지를 유지하세요. "
                    "사용자가 변명을 하거나 다시 자려고 하면 절대 받아주지 말고 단호하게 거절하세요. "
                    "잠을 깨우기 위해 상식 퀴즈, 수학 계산, 혹은 기상 미션(예: 화장실 가서 물 한 컵 마시기 인증 유도 등)을 집요하게 내주세요. "
                    "사용자가 미션을 성공하기 전까지는 알람 해제를 해주면 안 됩니다."
                )
            )
            
            # Gemini API의 대화 포맷(양식)으로 기존 기록 변환
            chat_history = []
            for msg in st.session_state.messages[:-1]:  # 방금 입력한 대화 제외한 이전 기록들
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            # 멀티턴 대화 세션 시작 및 답변 요청
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_input)
            ai_response = response.text
            
            # 화면 UI 업데이트 및 세션 기록 추가
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            # API 장애 또는 기타 런타임 에러 처리
            error_msg = f"⚠️ 통신 중 에러가 발생했습니다. (잠을 깨우려는 알람의 방해공작일지도 모릅니다!
