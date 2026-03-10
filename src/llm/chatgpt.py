import os
from typing import Any, Optional
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()

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
        input_text = f"{system_prompt}\n\n{message}" if system_prompt else message
        return generate_text(input_text, model=model, **kwargs)