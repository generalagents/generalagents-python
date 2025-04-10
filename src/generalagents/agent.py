import base64
import os
from io import BytesIO

import cattrs
import httpx
from PIL import Image

from generalagents.action import Action, ActionKind


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
        """A Session for interacting with the GeneralAgents API.

        Args:
            model: The model identifier to use for predictions.
            api_key: The API key for authentication.
            base_url: The base URL of the GeneralAgents API.
            instruction: The instruction to guide the agent's behavior.
            temperature: Sampling temperature for controlling randomness (0.0-1.0).
            max_previous_actions: Maximum number of previous actions to include in context.
        """
        self.model = model
        self.instruction = instruction
        self.max_previous_actions = max_previous_actions
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self.previous_actions = []
        self.temperature = temperature

    def plan(
        self,
        observation: Image.Image,
        *,
        allowed_action_kinds: list[ActionKind] | None = None,
    ) -> Action:
        """Plan the next action based on the current screen observation.

        Args:
            observation: Screenshot of the current screen state as a PIL Image.
            allowed_action_kinds: Optional list of action kinds to restrict the model to.
                If None, all action kinds are allowed.

        Returns:
            An Action object representing the next action to perform.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        buffer = BytesIO()
        observation.save(buffer, format="WEBP")
        image_url = f"data:image/webp;base64,{base64.b64encode(buffer.getvalue()).decode('utf8')}"

        data = {
            "model": self.model,
            "instruction": self.instruction,
            "image_url": image_url,
            "previous_actions": self.previous_actions[-self.max_previous_actions :],
            "temperature": self.temperature,
            "allowed_action_kinds": allowed_action_kinds,
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
        """Initialize an Agent for computer control.

        Args:
            model: The model identifier to use for predictions.
            api_key: The API key for authentication. Defaults to GENERALAGENTS_API_KEY
                environment variable.
            base_url: The base URL of the GeneralAgents API.
            temperature: Sampling temperature for controlling randomness (0.0-1.0).
            max_previous_actions: Maximum number of previous actions to include in context.

        Raises:
            ValueError: If no API key is provided and the environment variable is not set.
        """
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
        """Start a new session with the specified instruction.

        Args:
            instruction: The instruction to guide the agent's behavior.

        Returns:
            A Session object configured with this agent's parameters.
        """
        return Session(
            self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            instruction=instruction,
            temperature=self.temperature,
            max_previous_actions=self.max_previous_actions,
        )
