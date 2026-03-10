import streamlit as st
import requests

url = "http://localhost:8000/basic" 

st.title("KT front/back template chat")
st.caption("🚀 A Streamlit chatbot")

with st.sidebar:
    st.title("🤖 Model Settings")
    
    # 모델 선택 박스 (selectbox)
    model_name = st.selectbox(
        "사용할 모델을 선택하세요:",
        (
            "gpt-4o", 
            "gpt-4o-mini", 
            "gpt-5-mini", 
            "claude",
            "kt_agent_builder"
        ),
        index=0  # 기본값 설정 (0은 첫 번째 옵션)
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    payload = {
        "message": prompt,
        "model": model_name, 
        "system_prompt": "너는 KT Midm 모델이야" ## 추후 변경 
    }

    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result_data = response.json()
            answer = result_data["content"] 
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
        else:
            st.error(f"서버 에러: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("FastAPI 서버가 꺼져 있습니다. 서버를 먼저 실행해 주세요!")
