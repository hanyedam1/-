import streamlit as st
import random
import time

st.set_page_config(page_title="공포의 알람", page_icon="💀")
st.title("💀 절대 못 자는 기괴한 알람")
st.subheader("제한 시간 내에 미션을 해결하세요!")

if "alarm_cleared" not in st.session_state:
    st.session_state.alarm_cleared = False
if "target_value" not in st.session_state:
    st.session_state.target_value = random.randint(5, 95)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# 변수명과 주소를 최대한 짧게 줄여서 잘림 방지
s_list = [
    "https://actions.google.com/sounds/v1/alarms/industrial_alarm_blare.ogg",
    "https://actions.google.com/sounds/v1/emergency/nuclear_siren.ogg",
    "https://actions.google.com/sounds/v1/horror/ghost_whisper.ogg",
    "https://actions.google.com/sounds/v1/foley/metal_screech.ogg",
    "https://actions.google.com/sounds/v1/animals/coyote_howl.ogg"
]

if not st.session_state.alarm_cleared:
    # 안전하게 한 줄로 소리 선택
    if "snd" not in st.session_state:
        st.session_state.snd = random.choice(s_list)
    
    st.audio(st.session_state.snd, format="audio/ogg", autoplay=True)
    st.error("😱 기괴한 알람 작동 중!!! 뇌를 깨우세요!")
    st.write("---")
    
    # 타이머 기능
    limit = 20
    elapsed = int(time.time() - st.session_state.start_time)
    remain = limit - elapsed

    if remain <= 0:
        st.markdown("### 💥 폭발! 미션 수치와 버튼 위치가 재조합됩니다!")
        st.session_state.target_value = random.randint(5, 95)
        st.session_state.start_time = time.time()
        if "snd" in st.session_state: del st.session_state.snd
        st.rerun()
    else:
        st.progress(remain / limit, text=f"⏳ 폭발까지 남은 시간: {remain}초")

    # 미션 숫자 범위 설정
    if "t_max" not in st.session_state:
        st.session_state.t_max = random.choice([150, 200, 250])
        st.session_state.target_value = random.randint(10, st.session_state.t_max - 10)
        
    target = st.session_state.target_value
    t_max = st.session_state.t_max
    
    st.info(f"🎯 슬라이더를 [ {target} ]
    
