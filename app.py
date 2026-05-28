import streamlit as st
import random

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="절대 못 자는 알람", page_icon="⏰")
st.title("🚨 무조건 정신 차리는 알람 게임")
st.subheader("알람을 해제하지 않으면 오늘 하루는 없습니다.")

# 2. 세션 상태 초기화 (게임 성공 여부 저장)
if "alarm_cleared" not in st.session_state:
    st.session_state.alarm_cleared = False

# 3. 매번 상상하지도 못한 소리(효과음) 무작위 선택
sound_urls = [
    "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "https://actions.google.com/sounds/v1/emergency/ambulance_siren.ogg",
    "https://actions.google.com/sounds/v1/cartoon/slide_whistle_up.ogg",
    "https://actions.google.com/sounds/v1/foley/crumple_plastic_bag.ogg"
]

# 4. 알람 해제 성공 전까지 게임 진행
if not st.session_state.alarm_cleared:
    # 무작위 소리 자동 재생
    chosen_sound = random.choice(sound_urls)
    st.audio(chosen_sound, format="audio/ogg", autoplay=True)
    st.warning("🔥 알람이 울리고 있습니다! 어서 해제 미션을 완료하세요!")

    st.write("---")
    st.markdown("### 🧩 [미션] 슬라이더를 정확한 위치로 이동시키세요!")

    # 목표 값 설정
    if "target_value" not in st.session_state:
        st.session_state.target_value = random.randint(10, 90)
    
    target = st.session_state.target_value
    st.info(f"🎯 목표 수치: **{target}** 로 슬라이더를 맞추세요!")

    # 슬라이더 조절 (시작 위치 무작위)
    start_pos = random.choice([0, 100])
    user_value = st.slider("정신 차리고 조절하세요", min_value=0, max_value=100, value=start_pos)

    # 무작위 위치에 버튼 배치
    col_pos = random.randint(1, 3)
    col1, col2, col3 = st.columns(3)

    button_clicked = False
    if col_pos == 1:
        with col1: button_clicked = st.button("💥 알람 해제!!")
    elif col_pos == 2:
        with col2: button_clicked = st.button("💥 알람 해제!!")
    else:
        with col3: button_clicked = st.button("💥 알람 해제!!")

    # 결과 검증
    if button_clicked:
        if user_value == target:
            st.session_state.alarm_cleared = True
            st.columns(1) # 레이아웃 정리용
            st.rerun()
        else:
            st.error(f"❌ 실패! 슬라이더 위치가 틀렸습니다. (현재 입력값: {user_value})")
            st.session_state.target_value = random.randint(10, 90)
            st.rerun()

# 5. 알람 해제 성공 화면 (에러 났던 부분 한 줄로 안전하게 처리)
else:
    st.balloons()
    st.success("🎉 축하합니다! 알람이 해제되었습니다. 좋은 하루 되세요!")
    
    if st.button("내일 아침을 위해 알람 다시 켜기"):
        del st.session_state.target_value
        st.session_state.alarm_cleared = False
        st.rerun()
