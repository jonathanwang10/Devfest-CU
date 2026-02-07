# coordinator.py
# Coordinator Agent (Claude Sonnet 4) via Dedalus

from typing import Optional
from enum import Enum
from pydantic import BaseModel
# TODO: from dedalus import DedalusRunner, Tool


class Scenario(str, Enum):
    NONE = "NONE"
    CPR = "CPR"
    SEVERE_BLEEDING = "SEVERE_BLEEDING"
    CHOKING = "CHOKING"


class ScenarioState(str, Enum):
    INACTIVE = "inactive"
    DETECTED = "detected"
    ACTIVE = "active"
    ENDED = "ended"


class CoordinatorState(BaseModel):
    """Tracks coordinator agent state across turns."""
    scenario: Scenario = Scenario.NONE
    scenario_state: ScenarioState = ScenarioState.INACTIVE
    confidence: float = 0.0
    user_confirmations: list[str] = []
    last_vlm_observation: Optional[dict] = None
    last_conversation: Optional[str] = None


class CoordinatorAgent:
    """
    Central reasoning agent that orchestrates VLM, PersonaPlex, and tools.

    Responsibilities:
    - Integrate VLM observations
    - Integrate PersonaPlex conversation
    - Determine active scenario (CPR, BLEEDING, CHOKING, NONE)
    - Execute tools based on playbooks
    - Enforce safety rules

    Uses Claude Sonnet 4 via Dedalus SDK.
    """

    def __init__(self, session_id: str, connection_manager):
        self.session_id = session_id
        self.connection_manager = connection_manager
        self.state = CoordinatorState()
        # TODO: Initialize Dedalus runner
        # self.runner = DedalusRunner(model="claude-sonnet-4-20250514")

    async def process_frame(self, vlm_observation: dict) -> None:
        """
        Process VLM observation and update state.

        Called every 2-3 seconds with scene analysis.
        """
        self.state.last_vlm_observation = vlm_observation

        # TODO: Feed to Dedalus runner for reasoning
        # The coordinator decides if scenario changed and what tools to execute

    async def process_conversation(self, user_transcript: str, response_transcript: str) -> None:
        """
        Process conversation turn from PersonaPlex.

        Used for user confirmations and natural dialogue.
        """
        self.state.last_conversation = user_transcript

        # Check for user confirmations
        # e.g., "not breathing" confirms CPR scenario

    async def execute_tool(self, tool_name: str, params: dict) -> None:
        """
        Execute a tool command.

        Sends command to client via WebSocket.
        """
        await self.connection_manager.send_tool_command(
            self.session_id,
            tool_name,
            params
        )

        # TODO: Log to Langfuse
        # TODO: Log to session store
