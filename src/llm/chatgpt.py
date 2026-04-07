import os
from collections.abc import Iterator
from typing import Any, Optional
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()


def build_input_text(message: str, system_prompt: Optional[str] = None) -> str:
    return f"{system_prompt}\n\n{message}" if system_prompt else message


def generate_text(input_text: str, *, model: Optional[str] = None, **kwargs: Any) -> str:
    """
    Generate text using the OpenAI Responses API

    Example:
        text = generate_text("Write a one-sentence bedtime story about a unicorn.")
        print(text)
    """
    response = client.responses.create(
        model=model,
        input=input_text,
        **kwargs,
    )
    
    try:
        return response.output_text  
    except Exception:
        return "GPT API Error"


class OpenAIProvider:
    """
    Adapter implementing the LLMProvider protocol using OpenAI Responses API.
    """

    def generate(self, *, message: str, model: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        input_text = build_input_text(message=message, system_prompt=system_prompt)
        return generate_text(input_text, model=model, **kwargs)

    def supports_stream(self, *, model: str) -> bool:
        return True

    def stream_generate(
        self,
        *,
        message: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterator[str]:
        input_text = build_input_text(message=message, system_prompt=system_prompt)

        with client.responses.stream(
            model=model,
            input=input_text,
            **kwargs,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta" and event.delta:
                    yield event.delta
