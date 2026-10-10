from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Optional


STOP_WORDS = {
    "a", "an", "and", "are", "about", "after", "all", "be", "can", "could",
    "do", "does", "did", "for", "from", "get", "give", "has", "have", "help",
    "how", "i", "in", "is", "it", "me", "many", "much", "my", "of", "on",
    "or", "our", "please", "should", "show", "tell", "that", "the", "then",
    "this", "to", "want", "we", "what", "when", "where", "which", "who", "why",
    "will", "with", "would", "you", "your",
}
SYNONYMS = {
    "add": "create",
    "make": "create",
}


def _tokenize(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    normalized = set()
    for token in tokens:
        if token in STOP_WORDS:
            continue
        if len(token) > 5 and token.endswith("ies"):
            token = f"{token[:-3]}y"
        elif len(token) > 5 and token.endswith(("sses", "xes", "zes", "ches", "shes")):
            token = token[:-2]
        elif len(token) > 4 and token.endswith("s"):
            token = token[:-1]
        token = SYNONYMS.get(token, token)
        normalized.add(token)
    return normalized


class FAQRetriever:
    """Small local TF-IDF retriever for the private product FAQ corpus."""

    def __init__(self, knowledge_path: Optional[Path] = None) -> None:
        path = knowledge_path or Path(__file__).resolve().parents[1] / "knowledge" / "faqs.json"
        self.faqs: list[dict[str, Any]] = []
        self.document_terms: list[set[str]] = []
        self.document_frequency: dict[str, int] = {}

        if not path.is_file():
            return

        self.faqs = json.loads(path.read_text(encoding="utf-8"))
        for faq in self.faqs:
            terms = _tokenize(faq["question"] + " " + " ".join(faq["keywords"]))
            self.document_terms.append(terms)
            for term in terms:
                self.document_frequency[term] = self.document_frequency.get(term, 0) + 1

    def retrieve(self, question: str) -> Optional[str]:
        query_terms = _tokenize(question)
        if not query_terms or not self.faqs:
            return None

        if len(query_terms) == 1:
            term = next(iter(query_terms))
            if self.document_frequency.get(term, 0) > 2:
                return None

        total_documents = len(self.faqs)

        def inverse_document_frequency(term: str) -> float:
            frequency = self.document_frequency.get(term, 0)
            return math.log(1 + (total_documents - frequency + 0.5) / (frequency + 0.5))

        query_weights = {term: inverse_document_frequency(term) for term in query_terms}
        query_norm = math.sqrt(sum(weight * weight for weight in query_weights.values()))
        best_score = 0.0
        best_faq: Optional[dict[str, Any]] = None

        for faq, document_terms in zip(self.faqs, self.document_terms):
            document_weights = {
                term: inverse_document_frequency(term) for term in document_terms
            }
            document_norm = math.sqrt(
                sum(weight * weight for weight in document_weights.values())
            )
            if not document_norm:
                continue

            shared_terms = query_terms & document_terms
            dot_product = sum(query_weights[term] * document_weights[term] for term in shared_terms)
            score = dot_product / (query_norm * document_norm) if query_norm else 0.0
            question_terms = _tokenize(faq["question"])
            question_coverage = sum(
                query_weights[term] for term in query_terms & question_terms
            ) / sum(query_weights.values())
            score += 0.15 * question_coverage
            if score > best_score:
                best_score = score
                best_faq = faq

        if best_faq is None or best_score < 0.20:
            return None
        return best_faq["answer"]


faq_retriever = FAQRetriever()