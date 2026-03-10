from typing import Optional
import requests

class KTAgentBuilderProvider:
    """

    """

    def generate(self, *, message: str, model: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        url = "https://midm.kt.com/api/v1/agent/agent/9e43854f-a508-4208-a55f-0f81494035f6/run"
        API_KEY = "agent-Q5OL0R1fzCOhdq0lmDrp6UOtlt0"

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }

        data = {
            "input_text": "안녕? 너의 이름은 뭐니?",
        }

        res = requests.post(url, headers=headers, json=data)

        return f"{res.text}"



