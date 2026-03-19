import os

import requests
import streamlit as st

st.set_page_config(page_title="Bioplate Chat", page_icon=":speech_balloon:")

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
chat_url = f"{api_base_url}/basic"

st.title("KT front/back template chat")
st.caption("🚀 A Streamlit chatbot")

with st.sidebar:
    st.title("🤖 Model Settings")
    st.caption(f"API 서버: {api_base_url}")

    model_name = st.selectbox(
        "사용할 모델을 선택하세요:",
        (
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-5-mini",
            "langgraph-gpt-4o-mini",
            "claude",
            "kt_agent_builder",
        ),
        index=0,
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
        "system_prompt": "You are a helpful AI assistant.",
    }

    try:
        response = requests.post(chat_url, json=payload, timeout=60)

        if response.status_code == 200:
            result_data = response.json()
            answer = result_data["content"]

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
        else:
            st.error(f"서버 에러: {response.status_code}")
            st.code(response.text)

    except requests.exceptions.ConnectionError:
        st.error("FastAPI 서버에 연결할 수 없습니다. API 컨테이너 상태를 확인해 주세요.")
    except requests.exceptions.Timeout:
        st.error("API 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.")
