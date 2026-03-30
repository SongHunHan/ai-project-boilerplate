# Bioplate

이 저장소는 **Streamlit + FastAPI** 기반의 기본 템플릿입니다.

## Run With Docker Compose

`.env` 파일을 준비한 뒤 아래 명령으로 프론트와 백엔드를 한 번에 실행할 수 있습니다.

```bash
cp .env.example .env
docker compose up --build
```

실행 후 접속 주소:

- FastAPI: `http://localhost:8000`
- Streamlit: `http://localhost:8501`

종료할 때는 아래 명령을 사용합니다.

```bash
docker compose down
```

## Notes

- `ui` 컨테이너는 `API_BASE_URL=http://api:8000`를 사용해 `api` 서비스에 연결합니다.
- 로컬에서 Docker 없이 Streamlit을 직접 실행하면 기본값으로 `http://localhost:8000/basic`를 호출합니다.
- 다른 환경 파일을 쓰려면 `BIOPLATE_ENV_FILE=.env.staging docker compose up --build` 형태로 지정할 수 있습니다.
- Streamlit 모델 선택에서 `langgraph-gpt-4o-mini`를 고르면 LangGraph 기반의 기초 agent 경로를 통해 응답합니다.

## Prompt Usage

## 컨텍스트: AI 프로젝트 보일러플레이트
이 저장소는 **Streamlit(프론트) + FastAPI(백엔드)** 로 AI 기능을 붙이기 위한 뼈대다.
### 아키텍처 (반드시 유지)
- **Streamlit** (`app/ui/`): HTTP 클라이언트만 사용. 비즈니스 로직·API 키·LLM 직접 호출은 여기 두지 않는다. 백엔드 URL은 환경변수 `API_BASE_URL` (Docker에서는 `http://api:8000`).
- **FastAPI** (`app/api/`): `main.py`에 앱 등록, `routers/`에 라우트, `schemas/`에 Pydantic 모델.
- **도메인·LLM** (`src/`): `engines/chat_service.py`가 생성 흐름을 오케스트레이션. 모델 문자열 분기는 `engines/llm_router.py`, 각 벤더/방식은 `src/llm/`의 Provider. LangGraph 등 에이전트 경로는 `src/agents/`와 `ChatService`의 분기와 맞출 것.
- **실행**: `docker compose`로 API(8000)와 UI(8501)가 분리되어 있다. 로컬 Streamlit만 띄울 때는 기본으로 `http://localhost:8000`을 향한다.
### 이번 프로젝트에서 할 일
- 프로젝트명/목적: [예: 사내 문서 Q&A, 고객 지원 챗봇]
- 주요 사용자 시나리오: [예: 파일 업로드 후 질문, 단순 멀티턴 채팅]
- API 측면: [기존 `POST /basic` 유지 / 새 엔드포인트 추가 / 스키마 필드 추가 등 구체적으로]
- UI 측면: [사이드바 옵션, 추가 페이지, 스트리밍 여부 등]
- LLM/에이전트: [사용할 모델·Provider 규칙, LangGraph 사용 여부]
### 구현 시 지침
- 기존 폴더 역할을 존중하고, 변경은 요구사항에 필요한 최소 범위로만 한다.
- 새 API는 Router → Schema → Service(또는 Provider) 순으로 추가한다.
- README/환경변수 예시에 새로 필요한 키가 있으면 `.env.example`과 설명을 함께 갱신한다.
위 구조를 전제로, [구체적 작업 목록]을 구현해 줘.