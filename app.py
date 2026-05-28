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
# 재생할 때마다 브라우저가 다른 소리를 타겟팅하도록 무작위 주소 생성
sound_urls = [
    "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",  # 디지털 알람
    "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",    # 기계식 종소리
    "https://actions.google.com/sounds/v1/emergency/ambulance_siren.ogg",       # 구급차 사이렌
    "https://actions.google.com/sounds/v1/cartoon/slide_whistle_up.ogg",        # 황당한 호루라기
    "https://actions.google.com/sounds/v1/foley/crumple_plastic_bag.ogg"        # 비닐봉지 구기는 소리 (소름 유발)
]

# 4. 알람 해제 성공 전까지는 계속 소리를 지르고 게임을 보여줌
if not st.session_state.alarm_cleared:
    
    # [소리 재생] 무작위로 소리를 골라 자동 재생 (autoplay=True)
    chosen_sound = random.choice(sound_urls)
    st.audio(chosen_sound, format="audio/ogg", autoplay=True)
    st.warning("🔥 알람이 울리고 있습니다! 어서 해제 미션을 완료하세요!")

    st.write("---")
    st.markdown("### 🧩 [미션] 슬라이더를 정확한 위치로 이동시키세요!")

    # 5. 매번 무작위로 바뀌는 목표 슬라이더 값 (예: 0~100 사이의 무작위 숫자)
    # 꼼수를 막기 위해 사용자가 볼 때마다 정답 위치가 바뀝니다.
    if "target_value" not in st.session_state:
        st.session_state.target_value = random.randint(10, 90)
    
    target = st.session_state.target_value
    st.info(f"🎯 목표 수치: **{target}** 로 슬라이더를 맞추세요!")

    # 사용자가 조절하는 슬라이더 (시작 위치도 무작위)
    start_pos = random.choice([0, 100])
    user_value = st.slider("정신 차리고 조절하세요", min_value=0, max_value=100, value=start_pos)

    # 6. 매번 무작위 위치에 배치되는 해제 버튼
    # 스트림릿의 컬럼(기둥) 기능을 이용해 버튼이 왼쪽, 중간, 오른쪽 중 무작위로 나타나게 합니다.
    col_pos = random.randint(1, 3)
    col1, col2, col3 = st.columns(3)

    if col_pos == 1:
        with col1: button_clicked = st.button("💥 알람 해제!!")
    elif col_pos == 2:
        with col2: button_clicked = st.button("💥 알람 해제!!")
    else:
        with col3: button_clicked = st.button("💥 알람 해제!!")

    # 7. 해제 검증 logic
    if button_clicked:
        if user_value == target:
            st.session_state.alarm_cleared = True
            st.rerun()  # 상태를 반영하기 위해 화면 새로고침
        else:
            st.error(f"❌ 실패! 슬라이더 위치가 틀렸습니다. (현재 입력값: {user_value})")
            # 실패하면 다시 정신 차리라고 목표값을 바꿔버림
            st.session_state.target_value = random.randint(10, 90)
            st.rerun()

# 8. 알람 해제 성공 시 화면
else:
    st.balloons()
    st.success("🎉 축하합니다! 알람이
  
