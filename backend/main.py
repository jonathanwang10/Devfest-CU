# main.py
# Modal app entry point

import modal
from services.websocket.gateway import app as fastapi_app

# Modal app definition
# TODO: Configure with proper settings

stub = modal.App("first-aid-coach")

# Modal image with dependencies
image = modal.Image.debian_slim().pip_install(
    "fastapi",
    "uvicorn",
    "websockets",
    "openai",
    "anthropic",
    "langfuse",
    "supabase",
    "pydantic",
)


@stub.function(image=image)
@modal.asgi_app()
def web_app():
    """
    FastAPI ASGI app for WebSocket gateway.

    Deployed as a web endpoint on Modal.
    """
    return fastapi_app


# GPU function for PersonaPlex
# @stub.function(
#     image=image.pip_install("personaplex"),  # TODO: actual package
#     gpu="A10G",
#     timeout=300
# )
# async def personaplex_worker(audio_b64: str, scene_context: str, message: str = None):
#     from services.personaplex.worker import PersonaPlexWorker
#     worker = PersonaPlexWorker()
#     result = await worker.process_audio(audio_b64, scene_context, message)
#     return result.model_dump()


# VLM worker function
# @stub.function(image=image, timeout=60)
# async def vlm_worker(frame_b64: str):
#     from services.vlm.worker import VLMWorker
#     worker = VLMWorker()
#     result = await worker.analyze_frame(frame_b64)
#     return result.model_dump()


if __name__ == "__main__":
    # Local development
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
