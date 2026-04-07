from collections.abc import Iterator
from typing import Optional
import anthropic

client = anthropic.Anthropic()

class ClaudeProvider:
    """
    Stub provider for Anthropic Claude.
    Replace implementation with real Anthropic SDK calls when ready.
    """

    def generate(self, *, message: str, model: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        prompt = f"{system_prompt}\n\n{message}" if system_prompt else message

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ]
        )

        
        return f"[Claude stub:{model}] {message.content}"

    def supports_stream(self, *, model: str) -> bool:
        return False

    def stream_generate(
        self,
        *,
        message: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterator[str]:
        raise NotImplementedError(f"Streaming is not supported for model '{model}'.")
