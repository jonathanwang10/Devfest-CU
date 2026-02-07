# store.py
# Session store and event logging (Postgres/Supabase)

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum
# TODO: from supabase import create_client, Client


class SessionStatus(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"


class EventType(str, Enum):
    FRAME_ANALYZED = "frame_analyzed"
    CONVERSATION_TURN = "conversation_turn"
    SCENARIO_DETECTED = "scenario_detected"
    TOOL_CALLED = "tool_called"
    USER_CONFIRMED = "user_confirmed"


class Session(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    status: SessionStatus
    created_at: datetime
    ended_at: Optional[datetime] = None


class SessionEvent(BaseModel):
    session_id: str
    timestamp: datetime
    event_type: EventType
    payload: dict


class SessionStore:
    """
    Manages session state and event logging.

    Tables:
    - sessions: session_id, user_id, status, created_at, ended_at
    - events: session_id, timestamp, event_type, payload (append-only)
    """

    def __init__(self):
        # TODO: Initialize Supabase client
        # self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        pass

    async def create_session(self, session_id: str, user_id: Optional[str] = None) -> Session:
        """Create a new session."""
        # TODO: Insert into sessions table
        return Session(
            session_id=session_id,
            user_id=user_id,
            status=SessionStatus.ACTIVE,
            created_at=datetime.utcnow()
        )

    async def end_session(self, session_id: str) -> None:
        """Mark session as ended."""
        # TODO: Update session status and ended_at
        pass

    async def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve session by ID."""
        # TODO: Query sessions table
        return None

    async def log_event(
        self,
        session_id: str,
        event_type: EventType,
        payload: dict
    ) -> SessionEvent:
        """
        Log an event to the append-only event log.

        Events are used for:
        - Replay timeline in the app
        - Demo observability
        - Debugging and auditing
        """
        event = SessionEvent(
            session_id=session_id,
            timestamp=datetime.utcnow(),
            event_type=event_type,
            payload=payload
        )
        # TODO: Insert into events table
        return event

    async def get_session_events(self, session_id: str) -> list[SessionEvent]:
        """Retrieve all events for a session (for replay)."""
        # TODO: Query events table ordered by timestamp
        return []
