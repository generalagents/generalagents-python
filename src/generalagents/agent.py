import base64
import os
from io import BytesIO

import cattrs
import httpx
from PIL import Image

from generalagents.action import Action


class Session:
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
        instruction: str,
        temperature: float,
        max_previous_actions: int,
    ):
        """"""
        self.model = model
        self.instruction = instruction
        self.max_previous_actions = max_previous_actions
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self.previous_actions = []
        self.temperature = temperature

    def plan(self, observation: Image.Image) -> Action:
        buffer = BytesIO()
        observation.save(buffer, format="WEBP")
        image_url = f"data:image/webp;base64,{base64.b64encode(buffer.getvalue()).decode('utf8')}"

        data = {
            "model": self.model,
            "instruction": self.instruction,
            "image_url": image_url,
            "previous_actions": self.previous_actions[-self.max_previous_actions :],
            "temperature": self.temperature,
        }

        res = self.client.post("/v1/control/predict", json=data)
        res.raise_for_status()

        action = res.json()["action"]
        self.previous_actions.append(action)
        return cattrs.structure(action, Action)  # pyright: ignore [reportArgumentType] https://peps.python.org/pep-0747


class Agent:
    def __init__(
        self,
        model: str,
        api_key: str = os.getenv("GENERALAGENTS_API_KEY", ""),
        base_url: str = "https://api.generalagents.com",
        temperature: float = 0.3,
        max_previous_actions: int = 20,
    ):
        """"""
        if not api_key:
            msg = (
                "No API key provided, please set an environment variable "
                "GENERALAGENTS_API_KEY or provide it to the Agent constructor"
            )
            raise ValueError(msg)
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_previous_actions = max_previous_actions

    def start(self, instruction: str) -> Session:
        return Session(
            self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            instruction=instruction,
            temperature=self.temperature,
            max_previous_actions=self.max_previous_actions,
        )
