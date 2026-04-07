from collections.abc import Iterator
from typing import Optional, Protocol


class LLMProvider(Protocol):
    """
    Minimal provider interface for text generation.
    """

    def generate(self, *, message: str, model: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        ...

    def supports_stream(self, *, model: str) -> bool:
        ...

    def stream_generate(
        self,
        *,
        message: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterator[str]:
        ...
