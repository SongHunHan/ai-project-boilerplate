from __future__ import annotations

from functools import lru_cache
from typing import Any, Optional

from langgraph.graph import END, START, StateGraph

from src.engines.llm_router import select_provider


LANGGRAPH_PREFIX = "langgraph-"
DEFAULT_AGENT_MODEL = "gpt-4o-mini"


class AgentState(dict):
    """State container for the basic LangGraph agent."""


def is_langgraph_model(model: str) -> bool:
    return model.lower().startswith(LANGGRAPH_PREFIX)


def resolve_langgraph_model(model: str) -> str:
    if not is_langgraph_model(model):
        return model

    resolved = model[len(LANGGRAPH_PREFIX) :].strip()
    return resolved or DEFAULT_AGENT_MODEL


class BasicLangGraphAgent:
    """
    Minimal LangGraph agent that normalizes input, then calls the selected LLM.
    """

    def __init__(self) -> None:
        graph = StateGraph(dict)
        graph.add_node("prepare_input", self._prepare_input)
        graph.add_node("generate_response", self._generate_response)
        graph.add_edge(START, "prepare_input")
        graph.add_edge("prepare_input", "generate_response")
        graph.add_edge("generate_response", END)
        self._graph = graph.compile()

    def run(
        self,
        *,
        message: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        final_state = self._graph.invoke(
            {
                "message": message,
                "model": model,
                "system_prompt": system_prompt,
                "kwargs": kwargs,
            }
        )
        return final_state["response"]

    def _prepare_input(self, state: dict[str, Any]) -> dict[str, Any]:
        message = str(state["message"]).strip()
        if not message:
            raise ValueError("message must not be empty")

        base_system_prompt = "You are a helpful AI assistant. my name is songhunhan".strip()
        request_system_prompt = str(state.get("system_prompt") or "").strip()
        system_prompt = (
            f"{base_system_prompt}\n\n{request_system_prompt}"
            if request_system_prompt
            else base_system_prompt
        )

        return {
            "message": message,
            "model": state["model"],
            "system_prompt": system_prompt,
            "kwargs": state.get("kwargs", {}),
        }

    def _generate_response(self, state: dict[str, Any]) -> dict[str, Any]:
        model = str(state["model"])
        client = select_provider(model=model)
        response = client.generate(
            message=state["message"],
            model=model,
            system_prompt=state["system_prompt"],
            **state.get("kwargs", {}),
        )
        return {"response": response}


@lru_cache(maxsize=1)
def get_langgraph_agent() -> BasicLangGraphAgent:
    return BasicLangGraphAgent()
