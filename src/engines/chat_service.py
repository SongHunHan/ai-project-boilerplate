from typing import Optional
from src.engines.llm_router import select_provider


class ChatService:
    """
    Orchestrates text generation via provider selection.
    """

    def generate(
        self,
        *,
        message: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> dict[str, str]:
        client = select_provider(model=model)
        content = client.generate(message=message, model=model, system_prompt=system_prompt, **kwargs)
        return {"content": content, "model": model}