from __future__ import annotations

from typing import Optional


class LocalProvider:
    """
    Stub provider for local models (e.g., llama.cpp/gguf).
    Replace with your local inference pipeline.
    """

    def generate(self, *, message: str, model: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        prompt = f"{system_prompt}\n\n{message}" if system_prompt else message
        return f"[Local stub:{model}] {prompt}"
