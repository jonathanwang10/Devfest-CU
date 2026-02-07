# worker.py
# VLM (GPT-4o Vision) worker service

import base64
from typing import Optional
from pydantic import BaseModel
# TODO: import openai
# TODO: import modal


class VLMObservation(BaseModel):
    """Structured output from VLM scene analysis."""
    observations: str  # Natural language description
    visible_cues: list[str]  # e.g., ["unresponsive", "blood", "pale_skin"]
    confidence: float  # 0.0 to 1.0
    risk_flags: list[str]  # e.g., ["severe_bleeding", "unconscious"]


class VLMWorker:
    """
    Wraps OpenAI GPT-4o Vision API for scene analysis.

    Input: Blurred frame (base64 JPEG)
    Output: Structured observations for coordinator agent
    """

    SYSTEM_PROMPT = """You are analyzing video frames from a first-aid assistance system.
Your role is to identify emergency situations from visual cues.

IMPORTANT:
- You are NOT diagnosing medical conditions
- You are only describing observable visual cues
- Be conservative with confidence scores
- Flag any high-risk indicators

Output a JSON object with:
- observations: brief natural language description of the scene
- visible_cues: list of observable indicators (e.g., "person on ground", "blood visible", "not moving")
- confidence: how confident you are in the observation (0.0-1.0)
- risk_flags: any high-risk indicators (e.g., "unconscious", "severe_bleeding", "choking_gesture")

Focus only on what you can directly observe. Do not speculate or diagnose."""

    def __init__(self):
        # TODO: Initialize OpenAI client
        # self.client = openai.AsyncClient()
        pass

    async def analyze_frame(self, frame_b64: str) -> VLMObservation:
        """
        Analyze a video frame and return structured observations.

        Args:
            frame_b64: Base64-encoded JPEG image (already blurred for privacy)

        Returns:
            VLMObservation with scene analysis
        """
        # TODO: Implement GPT-4o Vision API call
        # response = await self.client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[
        #         {"role": "system", "content": self.SYSTEM_PROMPT},
        #         {
        #             "role": "user",
        #             "content": [
        #                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"}}
        #             ]
        #         }
        #     ],
        #     response_format={"type": "json_object"},
        #     max_tokens=500
        # )

        # Placeholder return
        return VLMObservation(
            observations="",
            visible_cues=[],
            confidence=0.0,
            risk_flags=[]
        )


# Modal deployment stub
# @modal.function(gpu="any")  # GPU optional for VLM, but useful for batching
# async def analyze_scene(frame_b64: str) -> dict:
#     worker = VLMWorker()
#     result = await worker.analyze_frame(frame_b64)
#     return result.model_dump()
