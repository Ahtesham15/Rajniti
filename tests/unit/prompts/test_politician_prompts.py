"""Unit tests for PoliticianPrompts."""

from app.prompts.politician_prompts import PoliticianPrompts

_BASE = {
    "id": "p1",
    "name": "Arjun Sharma",
    "type": "MP",
    "state": "Rajasthan",
    "constituency": "Jaipur",
    "political_background": {
        "elections": [
            {
                "year": 2024,
                "type": "MP",
                "state": "Rajasthan",
                "constituency": "Jaipur",
                "party": "INC",
                "status": "WON",
            }
        ],
        "summary": "Veteran Congress leader.",
    },
    "education": [
        {
            "qualification": "BACHELOR",
            "institution": "Delhi Uni",
            "year_completed": 1995,
        }
    ],
    "criminal_records": [
        {"name": "Corruption case", "type": "CORRUPTION", "year": 2015}
    ],
    "family_background": [{"name": "Meena Sharma", "relation": "WIFE"}],
    "contact": {"email": "arjun@example.com", "phone": None, "address": None},
    "social_media": {"twitter": "https://twitter.com/arjun", "website": None},
}


class TestSummaryPrompt:
    def test_contains_name(self):
        prompt = PoliticianPrompts.summary(_BASE)
        assert "Arjun Sharma" in prompt

    def test_contains_party(self):
        prompt = PoliticianPrompts.summary(_BASE)
        assert "INC" in prompt

    def test_contains_education(self):
        prompt = PoliticianPrompts.summary(_BASE)
        assert "BACHELOR" in prompt

    def test_contains_criminal_count(self):
        prompt = PoliticianPrompts.summary(_BASE)
        assert "Criminal cases: 1" in prompt

    def test_empty_politician_does_not_raise(self):
        prompt = PoliticianPrompts.summary({})
        assert isinstance(prompt, str)
        assert len(prompt) > 0


class TestAskPrompt:
    def test_contains_question(self):
        prompt = PoliticianPrompts.ask(_BASE, "What is his education?")
        assert "What is his education?" in prompt

    def test_contains_name(self):
        prompt = PoliticianPrompts.ask(_BASE, "Q?")
        assert "Arjun Sharma" in prompt

    def test_contains_election_record(self):
        prompt = PoliticianPrompts.ask(_BASE, "Q?")
        assert "INC" in prompt
        assert "WON" in prompt

    def test_contains_criminal_record(self):
        prompt = PoliticianPrompts.ask(_BASE, "Q?")
        assert "Corruption case" in prompt

    def test_contains_family(self):
        prompt = PoliticianPrompts.ask(_BASE, "Q?")
        assert "Meena Sharma" in prompt

    def test_contains_ai_summary_when_present(self):
        p = {**_BASE, "ai_summary": "Pre-computed AI insight."}
        prompt = PoliticianPrompts.ask(p, "Q?")
        assert "Pre-computed AI insight." in prompt

    def test_no_ai_summary_section_when_absent(self):
        prompt = PoliticianPrompts.ask(_BASE, "Q?")
        assert "AI Summary:" not in prompt

    def test_empty_politician_does_not_raise(self):
        prompt = PoliticianPrompts.ask({}, "Any question?")
        assert "Any question?" in prompt
