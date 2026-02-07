# definitions.py
# Tool definitions for Dedalus coordinator agent

from typing import Any

# Tool definitions for Dedalus SDK
# These define what tools the coordinator agent can call

TOOL_DEFINITIONS = [
    {
        "name": "analyze_scene",
        "description": "Analyze video frame to understand emergency situation. Returns structured observations about visible scene elements, confidence level, and risk flags.",
        "parameters": {
            "type": "object",
            "properties": {
                "frame_b64": {
                    "type": "string",
                    "description": "Base64 encoded JPEG image frame"
                }
            },
            "required": ["frame_b64"]
        }
    },
    {
        "name": "converse_with_user",
        "description": "Have natural voice conversation with the user via PersonaPlex. Use for questions, clarifications, encouragement, and guidance.",
        "parameters": {
            "type": "object",
            "properties": {
                "audio": {
                    "type": "string",
                    "description": "Base64 encoded user audio bytes"
                },
                "scene_context": {
                    "type": "string",
                    "description": "Current scene observations for context"
                },
                "message": {
                    "type": "string",
                    "description": "Specific message to communicate to user"
                }
            },
            "required": ["scene_context"]
        }
    },
    {
        "name": "start_metronome",
        "description": "Start audio metronome for CPR timing. Standard CPR rate is 100-120 BPM.",
        "parameters": {
            "type": "object",
            "properties": {
                "bpm": {
                    "type": "integer",
                    "description": "Beats per minute (100-120 for CPR)",
                    "minimum": 60,
                    "maximum": 180
                }
            },
            "required": ["bpm"]
        }
    },
    {
        "name": "stop_metronome",
        "description": "Stop the running metronome.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "start_timer",
        "description": "Start a countdown timer with a label. Shows countdown on UI and alerts when complete.",
        "parameters": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Timer label (e.g., 'switch_rescuer', 'pressure_check')"
                },
                "seconds": {
                    "type": "integer",
                    "description": "Duration in seconds",
                    "minimum": 10,
                    "maximum": 600
                }
            },
            "required": ["label", "seconds"]
        }
    },
    {
        "name": "stop_timer",
        "description": "Stop a specific timer by label.",
        "parameters": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Timer label to stop"
                }
            },
            "required": ["label"]
        }
    },
    {
        "name": "play_audio",
        "description": "Play audio instruction through the glasses speaker. PersonaPlex converts text to calm, clear speech. Keep messages short (1-2 sentences max).",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to speak (max 2 sentences)",
                    "maxLength": 200
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "show_ui",
        "description": "Display a UI card on the phone screen. Types: checklist (step-by-step instructions), banner (important message), alert (urgent notification).",
        "parameters": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["checklist", "banner", "alert"],
                    "description": "UI card type"
                },
                "content": {
                    "type": "object",
                    "description": "UI content (items for checklist, message for banner/alert)"
                }
            },
            "required": ["type", "content"]
        }
    },
    {
        "name": "log_event",
        "description": "Log an important decision or action for observability and replay.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_type": {
                    "type": "string",
                    "enum": ["scenario_detected", "tool_called", "user_confirmed", "safety_check"],
                    "description": "Type of event"
                },
                "data": {
                    "type": "object",
                    "description": "Event data (scenario, confidence, tool params, etc.)"
                }
            },
            "required": ["event_type", "data"]
        }
    }
]


def get_tool_definitions() -> list[dict[str, Any]]:
    """Return tool definitions for Dedalus SDK."""
    return TOOL_DEFINITIONS
