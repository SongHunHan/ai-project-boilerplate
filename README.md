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

# Task Instruction
1. 사용자의 업로드 문서에서 데이터를 추출 (이미지, 표)등을 이상없이 LLM이 이해하기 좋은 형태로 추출해야함
입력: 문서 (pdf등)
출력:
텍스트 (image, table등이 순차적으로 처리된 정보)
목적:
입력 문서 파싱
참고사항:
- 이미지 및 표 등을 LLM이 읽기 좋은 형태로 두기 위해 단순 PDF 파서보다 **Docling**을 활용한다.
    - 현재는 아래 코드로 이미지를 제외한 표, 텍스트만 추출
    """from docling.document_converter import DocumentConverter
    source = "input document" 
    converter = DocumentConverter()
    result = converter.convert(source)
    print(result.document.export_to_markdown())"""
    
    - **기본(빠름)**: `DocumentConverter()`만 쓰면 마크다운에 그림은 주로 `<!-- image -->` 플레이스홀더로 남고, 텍스트·표 중심이다.
    - **그림 설명 포함(느림, 로컬 VLM)**: `PdfPipelineOptions(do_picture_description=True)`와 `PdfFormatOption`을 `format_options`로 넘기면 그림 영역에 설명(어노테이션)을 붙일 수 있다. 프로토타입은 루트의 `test.py`를 참고한다.


세부 구현사항
- ui 페이지에 sidebar에 문서 upload 구역 생성
- 문서 upload시 관련 간단 정보 출력
- sidebar에 image 파싱 처리 여부 체크 항목 만들기
- 이미 파싱을 완료한 파일이 들어올 때 고려하여 ui 제작

## 이번 작업의 범위 명확화
- 이번 단계의 구현 범위는 문서 업로드, 문서 파싱 단계이다.
- 이 작업이 끝나고 다른 기능을 추가 구현 예정이므로, 폴더 구조 명확하게 기능단위로 분리(in src)

#README는 수정하지 말 것 