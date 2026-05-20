import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime

st.title("🩺 당뇨 건강 관리 챗봇")
st.write("AI 기반 맞춤형 식습관 및 운동 코칭 서비스")

# API 키 입력
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("API 키를 입력해주세요.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "당신은 당뇨병 환자의 식습관과 운동을 관리하는 전문 건강 코치입니다..."
    }]
    st.session_state.glucose_records = []

# 사이드바: 프로필 및 혈당 기록
with st.sidebar:
    st.header("👤 프로필 설정")
    st.session_state.profile = {
        "age": st.number_input("나이", 10, 100, 50),
        "weight": st.number_input("체중(kg)", 30.0, 200.0, 70.0),
        "type": st.selectbox("당뇨 유형", ["제2형", "제1형", "임신성"])
    }
    
    st.header("📊 혈당 기록")
    glucose = st.number_input("혈당(mg/dL)", 50, 400, 100)
    if st.button("기록"):
        st.session_state.glucose_records.append({
            "date": datetime.now(), "value": glucose
        })
    
    if st.session_state.glucose_records:
        df = pd.DataFrame(st.session_state.glucose_records)
        st.line_chart(df.set_index("date"))

# 채팅 인터페이스
for message in st.session_state.messages[1:]:  # system 메시지 제외
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("식단이나 운동에 대해 물어보세요"):
    # 프로필 정보를 컨텍스트에 추가
    profile_info = f"[프로필: {st.session_state.profile['age']}세, {st.session_state.profile['weight']}kg, {st.session_state.profile['type']}]"
    full_prompt = f"{profile_info} {prompt}"
    
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-4",  # 또는 gpt-3.5-turbo
        messages=st.session_state.messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("⚠️ 이 서비스는 참고용이며, 의학적 조언을 대체할 수 없습니다.")
