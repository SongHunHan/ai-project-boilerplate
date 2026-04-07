from collections.abc import Iterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.api.schemas.chat import ChatRequest, ChatResponse
from src.engines.chat_service import ChatService

router = APIRouter()


@router.post("/basic", response_model=ChatResponse)
async def chat_basic(
    req: ChatRequest,
) -> ChatResponse:
    svc = ChatService()

    result = svc.generate(
        message=req.message,
        model=req.model,
        system_prompt=req.system_prompt,
    )
    return ChatResponse(**result)


@router.post("/basic/stream")
async def chat_basic_stream(req: ChatRequest) -> StreamingResponse:
    svc = ChatService()

    if not svc.supports_stream(model=req.model):
        raise HTTPException(status_code=400, detail=f"Model '{req.model}' does not support streaming.")

    def stream_content() -> Iterator[str]:
        try:
            yield from svc.stream_generate(
                message=req.message,
                model=req.model,
                system_prompt=req.system_prompt,
            )
        except Exception as exc:
            yield f"\n[stream error] {exc}"

    return StreamingResponse(stream_content(), media_type="text/plain")
