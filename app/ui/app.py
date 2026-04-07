import os

import requests
import streamlit as st

st.set_page_config(page_title="Bioplate Chat", page_icon=":speech_balloon:")

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
chat_url = f"{api_base_url}/basic"
chat_stream_url = f"{api_base_url}/basic/stream"


def supports_stream(model: str) -> bool:
    lower = model.lower()
    if lower.startswith("langgraph-"):
        lower = lower[len("langgraph-") :]
    return lower.startswith(("gpt-", "gpt_", "gpt"))


def stream_chat_response(payload: dict[str, str]):
    with requests.post(chat_stream_url, json=payload, timeout=(10, 300), stream=True) as response:
        if response.status_code != 200:
            raise RuntimeError(f"서버 에러: {response.status_code}\n{response.text}")

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk

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

    stream_supported = supports_stream(model_name)
    use_stream = st.checkbox(
        "스트리밍 응답 사용",
        value=stream_supported,
        disabled=not stream_supported,
        help="지원 모델일 때만 응답을 토큰 단위로 화면에 표시합니다.",
    )
    if stream_supported:
        st.caption("선택한 모델은 스트리밍 응답을 지원합니다.")
    else:
        st.caption("선택한 모델은 현재 스트리밍을 지원하지 않아 일반 응답으로 동작합니다.")

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
        if use_stream and stream_supported:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                answer_chunks = []

                for chunk in stream_chat_response(payload):
                    answer_chunks.append(chunk)
                    placeholder.markdown("".join(answer_chunks) + "▌")

                answer = "".join(answer_chunks)
                placeholder.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
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
    except RuntimeError as exc:
        st.error(str(exc))
