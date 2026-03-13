"""Unit tests for PoliticianQAService."""

from unittest.mock import MagicMock

from app.services.politician_qa_service import PoliticianQAService


def _make_service(politician=None, llm_response="Test answer"):
    svc = PoliticianQAService.__new__(PoliticianQAService)
    mock_ps = MagicMock()
    mock_ps.get_by_id.return_value = politician
    mock_ps.update_politician.return_value = politician
    svc.politician_service = mock_ps

    mock_llm = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = llm_response
    mock_llm.invoke.return_value = mock_resp
    svc.llm = mock_llm

    return svc


_SAMPLE_POLITICIAN = {
    "id": "p1",
    "name": "Test Neta",
    "type": "MP",
    "state": "Maharashtra",
    "constituency": "Mumbai North",
    "political_background": {
        "elections": [
            {
                "year": 2024,
                "party": "BJP",
                "type": "MP",
                "state": "Maharashtra",
                "constituency": "Mumbai North",
                "status": "WON",
            }
        ],
        "summary": "Seasoned politician",
    },
    "education": [
        {
            "qualification": "BACHELOR",
            "institution": "Mumbai Uni",
            "year_completed": 2000,
        }
    ],
    "criminal_records": [],
    "family_background": [{"name": "Jane Neta", "relation": "WIFE"}],
    "contact": {"email": "neta@example.com", "phone": None, "address": None},
    "social_media": {"twitter": "https://twitter.com/neta", "website": None},
}


class TestAsk:
    def test_returns_answer_on_success(self):
        svc = _make_service(
            politician=_SAMPLE_POLITICIAN, llm_response="He won in 2024."
        )
        result = svc.ask("p1", "What party does he belong to?")
        assert result["success"] is True
        assert result["answer"] == "He won in 2024."
        assert result["politician_name"] == "Test Neta"

    def test_returns_error_when_politician_not_found(self):
        svc = _make_service(politician=None)
        result = svc.ask("bad-id", "Any question")
        assert result["success"] is False
        assert result["error"] == "Politician not found"

    def test_returns_error_when_question_empty(self):
        svc = _make_service(politician=_SAMPLE_POLITICIAN)
        result = svc.ask("p1", "")
        assert result["success"] is False
        assert "required" in result["error"].lower()

    def test_returns_error_when_llm_raises(self):
        svc = _make_service(politician=_SAMPLE_POLITICIAN)
        svc.llm.invoke.side_effect = RuntimeError("LLM timeout")
        result = svc.ask("p1", "Some question")
        assert result["success"] is False
        assert "LLM timeout" in result["error"]


class TestGenerateSummary:
    def test_returns_cached_summary_when_present(self):
        p = {**_SAMPLE_POLITICIAN, "ai_summary": "Already computed."}
        svc = _make_service(politician=p)
        result = svc.generate_summary("p1")
        assert result["success"] is True
        assert result["summary"] == "Already computed."
        assert result["cached"] is True
        svc.llm.invoke.assert_not_called()

    def test_generates_and_persists_summary_when_absent(self):
        svc = _make_service(
            politician=_SAMPLE_POLITICIAN, llm_response="Fresh summary."
        )
        result = svc.generate_summary("p1")
        assert result["success"] is True
        assert result["summary"] == "Fresh summary."
        assert result["cached"] is False
        svc.politician_service.update_politician.assert_called_once_with(
            "p1", {"ai_summary": "Fresh summary."}
        )

    def test_returns_error_when_politician_not_found(self):
        svc = _make_service(politician=None)
        result = svc.generate_summary("missing-id")
        assert result["success"] is False
        assert result["error"] == "Politician not found"

    def test_returns_error_when_llm_raises(self):
        svc = _make_service(politician=_SAMPLE_POLITICIAN)
        svc.llm.invoke.side_effect = RuntimeError("LLM down")
        result = svc.generate_summary("p1")
        assert result["success"] is False
        assert "LLM down" in result["error"]
