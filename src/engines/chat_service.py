from typing import Optional
from src.agents.langgraph_agent import get_langgraph_agent, is_langgraph_model, resolve_langgraph_model
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
        if is_langgraph_model(model):
            agent = get_langgraph_agent()
            resolved_model = resolve_langgraph_model(model)
            content = agent.run(
                message=message,
                model=resolved_model,
                system_prompt=system_prompt,
                **kwargs,
            )
            return {"content": content, "model": model}

        client = select_provider(model=model)
        content = client.generate(message=message, model=model, system_prompt=system_prompt, **kwargs)
        return {"content": content, "model": model}
