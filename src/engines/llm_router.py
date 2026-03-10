from src.engines.llm_provider import LLMProvider
from src.llm.chatgpt import OpenAIProvider
from src.llm.kt_agent_builder import KTAgentBuilderProvider
from src.llm.claude import ClaudeProvider
# from src.llm.local import LocalProvider

# Optional: future providers (uncomment when implemented)
# from src.llm.claude import ClaudeProvider



def select_provider(*, model: str) -> LLMProvider:
    """
    Select an LLM provider instance based on model prefix only.
      - startswith gpt-, gpt_  -> OpenAI
      - startswith claude-, anthropic- -> Claude
      - startswith local-, gguf-, llama- -> Local
    """
    lower = model.lower()
    if lower.startswith(("gpt-", "gpt_", "gpt")):
        return OpenAIProvider()
    if lower.startswith(("kt")):
        return KTAgentBuilderProvider()
    if lower.startswith(("claude", "anthropic-")):
        return ClaudeProvider()
    # if lower.startswith(("local-", "gguf-", "llama-")):
    #     return LocalProvider()
    # Default
    return OpenAIProvider()