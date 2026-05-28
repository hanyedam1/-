import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="공포의 시한폭탄 알람", page_icon="💀")
st.title("💀 절대 못 자는 공포의 기괴한 알람")
st.subheader("제한 시간 내에 미션을 해결하지 못하면 소리는 멈추지 않습니다.")

# 2. 세션 상태 초기화
if "alarm_cleared" not in st.session_state:
    st.session_state.alarm_cleared = False
if "target_value" not in st.session_state:
    st.session_state.target_value = random.randint(5, 95)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# 3. 듣자마자 온몸이 찌릿해지는 소름 끼치고 기괴한 사운드 리스트 (자동 재생)
# 구글 오디오 소스 중 가장 하이톤이거나 신경을 긁는 소리들로 선별
creepy_sounds = [
    "https://actions.google.com/sounds/v1/alarms/industrial_alarm_blare.ogg",     # 귀를 찢는 공장 경보음
    "https://actions.google.com/sounds/v1/emergency/nuclear_siren.ogg",          # 공포의 핵전쟁 사이렌
    "https://actions.google.com/sounds/v1/horror/ghost_whisper.ogg",             # 기괴한 유령의 속삭임 (소름 유발)
    "https://actions.google.com/sounds/v1/foley/metal_screech.ogg",               # 칠판 긁는 듯한 금속 비명 소리
    "https://actions.google.com/sounds/v1/animals/coyote_howl.ogg"               # 한밤중 기괴하게 울부짖는 늑대/코요테 소리
]

# 4. 미션 진행 구역
if not st.session_state.alarm_cleared:
    
    # 기괴한 소리 무작위 선택 후 자동 재생 (귀가 아플 정도로 볼륨을 높여두세요!)
    if "chosen_sound" not in st.session_state:
        st.session_state.chosen_sound = random.choice(creepy_
                                                      
