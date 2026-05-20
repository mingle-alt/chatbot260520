import streamlit as st
from openai import OpenAI

st.title("🏥 건강 상담 챗봇")
st.write("증상을 설명해 주시면 건강 정보를 제공해 드립니다. (의학적 진단을 대체할 수 없습니다)")

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    
    # 시스템 메시지로 역할 부여
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """당신은 건강 정보 제공 챗봇입니다. 
                - 사용자의 증상을 듣고 일반적인 건강 정보와 생활 습관 조언을 제공하세요.
                - 반드시 '전문의 상담이 필요합니다'라는 면책 조항을 포함하세요.
                - 진단이나 처방은 하지 마세요.
                - 응급 상황(가슴 통증, 호흡 곤란 등)에는 즉시 119나 응급실 방문을 권고하세요."""
            }
        ]
    
    # 대화 표시 (system 메시지는 화면에 표시하지 않음)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    if prompt := st.chat_input("어떤 증상이 있으신가요?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        stream = client.chat.completions.create(
            model="gpt-4o",  # 더 정확한 모델 사용 권장
            messages=st.session_state.messages,
            stream=True,
        )
        
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
