"""Politician Q&A Service — answers questions about a specific politician using LLM."""

import logging
from typing import Any, Dict

from app.config.agent_config import get_agent_llm
from app.prompts.politician_prompts import PoliticianPrompts
from app.services.politician_service import PoliticianService

logger = logging.getLogger(__name__)


class PoliticianQAService:
    """Answers free-form questions about a politician using their profile data + LLM."""

    def __init__(self) -> None:
        self.politician_service = PoliticianService()
        self.llm = get_agent_llm()

    def ask(self, politician_id: str, question: str) -> Dict[str, Any]:
        """Answer a question about a specific politician."""
        if not question or not question.strip():
            return {"success": False, "error": "Question is required"}

        politician = self.politician_service.get_by_id(politician_id)
        if not politician:
            return {"success": False, "error": "Politician not found"}

        prompt = PoliticianPrompts.ask(politician, question.strip())
        try:
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, "content") else str(response)
            return {
                "success": True,
                "question": question,
                "answer": answer.strip(),
                "politician_id": politician_id,
                "politician_name": politician.get("name", ""),
            }
        except Exception as exc:
            logger.error("PoliticianQAService.ask error: %s", exc)
            return {"success": False, "error": str(exc)}

    def generate_summary(self, politician_id: str) -> Dict[str, Any]:
        """Generate (or return cached) AI summary for a politician."""
        politician = self.politician_service.get_by_id(politician_id)
        if not politician:
            return {"success": False, "error": "Politician not found"}

        if politician.get("ai_summary"):
            return {
                "success": True,
                "summary": politician["ai_summary"],
                "politician_id": politician_id,
                "politician_name": politician.get("name", ""),
                "cached": True,
            }

        prompt = PoliticianPrompts.summary(politician)
        try:
            response = self.llm.invoke(prompt)
            summary = (
                response.content if hasattr(response, "content") else str(response)
            )
            summary = summary.strip()
            self.politician_service.update_politician(
                politician_id, {"ai_summary": summary}
            )
            return {
                "success": True,
                "summary": summary,
                "politician_id": politician_id,
                "politician_name": politician.get("name", ""),
                "cached": False,
            }
        except Exception as exc:
            logger.error("PoliticianQAService.generate_summary error: %s", exc)
            return {"success": False, "error": str(exc)}
