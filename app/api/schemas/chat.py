from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Simple request for text generation via Responses API.
    """
    message: str = Field(..., description="User message")
    system_prompt: Optional[str] = Field(None, description="System prompt (optional)")
    model: str = Field(..., description="Model to use, e.g., gpt-5-nano")


class ChatResponse(BaseModel):
    """
    Minimal response containing the generated content and model used.
    """
    content: str = Field(..., description="AI response content")