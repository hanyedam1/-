import streamlit as st
import random
import time

st.set_page_config(page_title="ALARM", page_icon="💀")
st.title("💀 ALARM GMS")

if "alarm_cleared" not in st.session_state:
    st.session_state.alarm_cleared = False
if "target_value" not in st.session_state:
    st.session_state.target_value = random.randint(5, 95)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

s_list = [
    "https://actions.google.com/sounds/v1/alarms/industrial_alarm_blare.ogg",
    "https://actions.google.com/sounds/v1/emergency/nuclear_siren.ogg",
    "https://actions.google.com/sounds/v1/horror/ghost_whisper.ogg",
    "https://actions.google.com/sounds/v1/foley/metal_screech.ogg",
    "https://actions.google.com/sounds/v1/animals/coyote_howl.ogg"
]

if not st.session_state.alarm_cleared:
    if "snd" not in st.session_state:
        st.session_state.snd = random.choice(s_list)
    
    st.audio(st.session_state.snd, format="audio/ogg", autoplay=True)
    st.error("!!! ALARM !!!")
    st.write("---")
    
    limit = 20
    elapsed = int(time.time() - st.session_state.start_time)
    remain = limit - elapsed

    if remain <= 0:
        st.write("BOOM! RESET!")
        st.session_state.target_value = random.randint(5, 95)
        st.session_state.start_time = time.time()
        if "snd" in st.session_state: del st.session_state.snd
        st.rerun()
    else:
        st.progress(remain / limit)
        st.write("Time:", remain)

    if "t_max" not in st.session_state:
        st.session_state.t_max = random.choice([150, 200, 250])
        st.session_state.target_value = random.randint(10, st.session_state.t_max - 10)
        
    target = st.session_state.target_value
    t_max = st.session_state.t_max
    
    # 에러 원인이던 f-string을 없애고 쉼표(,)로 안전하게 분리 출력
    st.info("GOAL VALUE IS BELOW")
    st.title(target)

    if "s_pos" not in st.session_state:
        st.session_state.s_pos = random.choice([0, t_max])
        
    u_val = st.slider("MOVE", 0, t_max, st.session_state.s_pos)

    col_pos = random.randint(1, 3)
    c1, c2, c3 = st.columns(3)

    click = False
    if col_pos == 1:
        with c1: click = st.button("CLICK 1")
    elif col_pos == 2:
        with c2: click = st.button("CLICK 2")
    else:
        with c3: click = st.button("CLICK 3")

    if click:
        if u_val == target:
            st.session_state.alarm_cleared = True
            if "snd" in st.session_state: del st.session_state.snd
            if "t_max" in st.session_state: del st.session_state.t_max
            st.rerun()
        else:
            st.error("WRONG! RESET!")
            st.session_state.target_value = random.randint(10, t_max - 10)
            st.rerun()

else:
    st.balloons()
    st.success("SUCCESS")
    if st.button("RESTART"):
        del st.session_state.target_value
        st.session_state.alarm_cleared = False
        st.rerun()
