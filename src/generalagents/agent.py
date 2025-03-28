import base64
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
        instruction: str,
        temperature: float,
        max_previous_actions: int,
    ):
        """"""
        self.model = model
        self.instruction = instruction
        self.max_previous_actions = max_previous_actions
        self.client = httpx.Client(
            base_url="https://api.generalagents.com",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self.previous_actions = []
        self.temperature = temperature

    def plan(self, observation: Image.Image) -> Action:
        buffer = BytesIO()
        observation.save(buffer, format="PNG")
        image_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf8')}"

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
        print(f"Received action {action}")
        return cattrs.structure(action, Action)  # pyright: ignore [reportArgumentType] https://peps.python.org/pep-0747


class Agent:
    def __init__(
        self,
        model: str,
        api_key: str,
        temperature: float = 0.3,
        max_previous_actions: int = 20,
    ):
        """"""
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_previous_actions = max_previous_actions

    def start(self, instruction: str) -> Session:
        return Session(
            self.model,
            api_key=self.api_key,
            instruction=instruction,
            temperature=self.temperature,
            max_previous_actions=self.max_previous_actions,
        )
