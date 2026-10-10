from __future__ import annotations

import re

from backend.config.logging_config import logger
from backend.services.faq_retriever import faq_retriever


class ChatbotService:
    """Placeholder chatbot engine that can later be replaced by an LLM or RAG service."""

    def generate_response(self, message: str) -> str:
        if not message or not message.strip():
            return "Sorry, please clarify."

        normalized = re.sub(r"\s+", " ", message.strip().lower())
        greeting_tokens = {"hello", "hi", "hey", "namaste", "greetings"}
        message_tokens = set(re.findall(r"[a-z]+", normalized))

        if message_tokens and message_tokens <= greeting_tokens:
            return "Hello. I am Babu, the VakilBabu assistant."

        answer = faq_retriever.retrieve(normalized)
        if answer:
            return answer

        logger.info("No FAQ match found for chat request")
        return "Sorry, please clarify."


chatbot_service = ChatbotService()
