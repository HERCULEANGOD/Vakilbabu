from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.config.logging_config import logger
from backend.models.chat import ChatRequest, ChatResponse, HealthResponse
from backend.services.chatbot_service import chatbot_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", app_name="Babu", version="0.1.0")


@router.post("/chat", response_model=ChatResponse)
async def create_chat_message(payload: ChatRequest) -> ChatResponse:
    try:
        response_text = chatbot_service.generate_response(payload.message)
        logger.info("Chat request processed successfully")
        return ChatResponse(response=response_text)
    except ValueError as exc:
        logger.warning("Bad chat request: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error while processing chat message")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while processing your message.",
        ) from exc
