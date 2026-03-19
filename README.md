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
