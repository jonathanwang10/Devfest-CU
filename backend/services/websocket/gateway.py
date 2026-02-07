# gateway.py
# FastAPI WebSocket gateway for client communication

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import asyncio

# TODO: Import orchestration engine
# from orchestration.engine import DedalusOrchestrator


app = FastAPI(title="First Aid Coach WebSocket Gateway")


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_tool_command(self, session_id: str, tool: str, params: dict):
        """Send tool command to client."""
        if session_id in self.active_connections:
            message = {
                "type": "tool_command",
                "tool": tool,
                "params": params
            }
            await self.active_connections[session_id].send_json(message)

    async def send_audio_response(self, session_id: str, audio_b64: str, transcript: str):
        """Send PersonaPlex audio response to client."""
        if session_id in self.active_connections:
            message = {
                "type": "audio_response",
                "audio_b64": audio_b64,
                "transcript": transcript
            }
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Main WebSocket endpoint for client communication.

    Receives:
    - Frame messages: { "type": "frame", "session_id": "...", "timestamp": ..., "frame_b64": "..." }
    - Audio messages: { "type": "audio", "session_id": "...", "timestamp": ..., "audio_b64": "..." }

    Sends:
    - Tool commands: { "type": "tool_command", "tool": "...", "params": {...} }
    - Audio responses: { "type": "audio_response", "audio_b64": "...", "transcript": "..." }
    """
    await manager.connect(websocket, session_id)

    # TODO: Initialize Dedalus orchestrator for this session
    # orchestrator = DedalusOrchestrator(session_id, manager)

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "frame":
                # TODO: Pass to orchestrator for VLM analysis
                # await orchestrator.process_frame(data["frame_b64"], data["timestamp"])
                pass

            elif message_type == "audio":
                # TODO: Pass to orchestrator for PersonaPlex conversation
                # await orchestrator.process_audio(data["audio_b64"], data["timestamp"])
                pass

            elif message_type == "heartbeat":
                await websocket.send_json({"type": "heartbeat_ack"})

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        # TODO: Clean up orchestrator session
