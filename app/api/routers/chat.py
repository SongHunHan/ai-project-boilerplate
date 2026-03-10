from fastapi import APIRouter, Depends

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