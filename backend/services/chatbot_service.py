from __future__ import annotations

import re
from typing import List

from backend.config.logging_config import logger


class ChatbotService:
    """Placeholder chatbot engine that can later be replaced by an LLM or RAG service."""

    APP_TOPICS = {
        "hello": ["hello", "hi", "hey", "namaste", "greetings"],
        "cases": ["case", "cases", "matter", "legal matter", "litigation"],
        "documents": ["document", "documents", "file", "files", "upload", "pdf"],
        "pricing": ["price", "pricing", "plan", "package", "subscription"],
        "account": ["login", "signup", "signin", "account", "profile", "register"],
        "support": ["support", "help", "assist", "contact", "team"],
    }

    def generate_response(self, message: str) -> str:
        if not message or not message.strip():
            return "Sorry, please clarify."

        normalized = re.sub(r"\s+", " ", message.strip().lower())

        if any(keyword in normalized for keyword in self.APP_TOPICS["hello"]):
            return "Hello. I am Bengoshi, the VakilBabu assistant."

        if any(keyword in normalized for keyword in self.APP_TOPICS["cases"]):
            return "I can help with case-related questions in the app."

        if any(keyword in normalized for keyword in self.APP_TOPICS["documents"]):
            return "Please upload or review documents in the workspace."

        if any(keyword in normalized for keyword in self.APP_TOPICS["pricing"]):
            return "Please check the pricing section in the app."

        if any(keyword in normalized for keyword in self.APP_TOPICS["account"]):
            return "The account section manages profile and access details."

        if any(keyword in normalized for keyword in self.APP_TOPICS["support"]):
            return "Please contact the support team through the app support page."

        logger.info("Received non-app-related query: %s", normalized)
        return "Sorry, please clarify."


chatbot_service = ChatbotService()
