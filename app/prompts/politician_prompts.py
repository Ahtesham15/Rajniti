from __future__ import annotations

from typing import Any, Dict


class PoliticianPrompts:
    """Central place for politician-related prompt builders."""

    @staticmethod
    def education(politician: Dict[str, Any]) -> str:
        """Build a strict JSON prompt for education extraction."""
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")

        return (
            "You are extracting structured data about an Indian politician.\n"
            "Return ONLY valid JSON array. Each item format:\n"
            '[{"qualification": "HIGH_SCHOOL|DIPLOMA|BACHELOR|MASTER|DOCTORATE|PROFESSIONAL|OTHERS|null", '
            '"institution": "string|null", "year_completed": number|null}]\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "If unknown, return []"
        )

    @staticmethod
    def political_background(politician: Dict[str, Any]) -> str:
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting a politician's political background.\n"
            "Return ONLY a valid JSON object matching this shape:\n"
            '{ "elections": [ { "year": 2024, "type": "MP|MLA", "state": "string", '
            '"constituency": "string", "party": "string", "status": "WON|LOST|CONTESTED" } ], '
            '"summary": "short textual summary or null" }\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            'If unknown, return {"elections": [], "summary": null}'
        )

    @staticmethod
    def political_background_elections_only(politician: Dict[str, Any]) -> str:
        """Focused prompt to extract elections array if missing/empty."""
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting ONLY the election history for this politician.\n"
            "Return ONLY a valid JSON array. Each item format:\n"
            '[{ "year": 2024, "type": "MP|MLA", "state": "string", "constituency": "string", '
            '"party": "string", "status": "WINNER|LOSER|INCUMBENT" }]\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "If unknown, return []"
        )

    @staticmethod
    def social_media(politician: Dict[str, Any]) -> str:
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting social media links for an Indian politician.\n"
            "Return ONLY a valid JSON object matching this shape:\n"
            '{"twitter": "url|null", "facebook": "url|null", "instagram": "url|null", '
            '"linkedin": "url|null", "youtube": "url|null", "website": "url|null"}\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "Only include verified/official links. "
            'If unknown, return {"twitter": null, "facebook": null, "instagram": null, '
            '"linkedin": null, "youtube": null, "website": null}'
        )

    @staticmethod
    def family_background(politician: Dict[str, Any]) -> str:
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting family background for an Indian politician.\n"
            "Return ONLY a valid JSON array. Each item format:\n"
            '[{"name": "string", '
            '"relation": "FATHER|MOTHER|SIBLING|SON|DAUGHTER|WIFE|HUSBAND|OTHERS", '
            '"photo": "url|null", "social_media": null}]\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "Only include publicly known family members. "
            "If unknown, return []"
        )

    @staticmethod
    def criminal_records(politician: Dict[str, Any]) -> str:
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting criminal records for an Indian politician.\n"
            "Return ONLY a valid JSON array. Each item format:\n"
            '[{"name": "brief case description", '
            '"type": "MURDER|RAPE|KIDNAPPING|THEFT|CORRUPTION|ECONOMIC|OTHERS|null", '
            '"year": number|null}]\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "Only include publicly reported and documented cases. Do not speculate. "
            "If unknown or none, return []"
        )

    @staticmethod
    def contact(politician: Dict[str, Any]) -> str:
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        return (
            "You are extracting contact information for an Indian politician.\n"
            "Return ONLY a valid JSON object matching this shape:\n"
            '{"email": "string|null", "phone": "string|null", "address": "string|null"}\n'
            f"Politician: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\n"
            "Only include officially published contact details. "
            'If unknown, return {"email": null, "phone": null, "address": null}'
        )

    @staticmethod
    def summary(politician: Dict[str, Any]) -> str:
        """Prompt to generate a narrative AI summary of the politician."""
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        elections = (politician.get("political_background") or {}).get(
            "elections"
        ) or []
        party = elections[0].get("party", "") if elections else ""
        education_list = politician.get("education") or []
        edu_str = ", ".join(
            e.get("qualification", "") for e in education_list if e.get("qualification")
        )
        criminal_count = len(politician.get("criminal_records") or [])
        family = politician.get("family_background") or []
        political_summary = (politician.get("political_background") or {}).get(
            "summary"
        ) or ""

        return (
            "You are writing a concise, factual profile summary for an Indian politician.\n"
            "Write 3-4 sentences covering: who they are, their political career, notable facts.\n"
            "Keep a neutral, informative tone. Do not speculate. Use only verified facts.\n"
            "Return ONLY the summary text, no JSON, no headings.\n\n"
            f"Name: {name}\n"
            f"Type: {ptype}\n"
            f"State: {state}\n"
            f"Constituency: {constituency}\n"
            f"Party: {party}\n"
            f"Education: {edu_str or 'Unknown'}\n"
            f"Criminal cases: {criminal_count}\n"
            f"Family members on record: {len(family)}\n"
            f"Political summary: {political_summary or 'Not available'}\n"
            f"Elections on record: {len(elections)}\n"
        )

    @staticmethod
    def ask(politician: Dict[str, Any], question: str) -> str:
        """Prompt to answer a user's question about a specific politician."""
        name = politician.get("name", "")
        state = politician.get("state", "")
        constituency = politician.get("constituency", "")
        ptype = politician.get("type", "")
        elections = (politician.get("political_background") or {}).get(
            "elections"
        ) or []
        party = elections[0].get("party", "") if elections else ""

        education_list = politician.get("education") or []
        edu_items = (
            "\n".join(
                f"  - {e.get('qualification', '')} from "
                f"{e.get('institution', '?')} ({e.get('year_completed', '?')})"
                for e in education_list
            )
            or "  - Not available"
        )

        criminal_records = politician.get("criminal_records") or []
        crimes_str = (
            "\n".join(
                f"  - {c.get('name', '')} [{c.get('type', '')}] ({c.get('year', '')})"
                for c in criminal_records
            )
            or "  - None on record"
        )

        family = politician.get("family_background") or []
        family_str = (
            "\n".join(
                f"  - {m.get('name', '')} ({m.get('relation', '')})" for m in family
            )
            or "  - Not available"
        )

        elections_str = (
            "\n".join(
                f"  - {e.get('year', '')} {e.get('type', '')} "
                f"{e.get('constituency', '')} "
                f"{e.get('state', '')} [{e.get('party', '')}] → {e.get('status', '')}"
                for e in elections
            )
            or "  - Not available"
        )

        political_summary = (politician.get("political_background") or {}).get(
            "summary"
        ) or "Not available"
        contact = politician.get("contact") or {}
        social = politician.get("social_media") or {}
        ai_summary = politician.get("ai_summary") or ""

        return (
            f"You are an expert assistant on Indian politics. Answer the user's question about {name}.\n"
            "Be factual, concise, and accurate. If you don't know, say so clearly.\n"
            "Only use the data below plus your own knowledge. Do not speculate.\n\n"
            "=== Politician Profile ===\n"
            f"Name: {name}\nType: {ptype}\nState: {state}\nConstituency: {constituency}\nParty: {party}\n\n"
            f"Education:\n{edu_items}\n\n"
            f"Political Career:\n{elections_str}\n"
            f"Summary: {political_summary}\n\n"
            f"Criminal Records:\n{crimes_str}\n\n"
            f"Family:\n{family_str}\n\n"
            f"Contact: {contact.get('email', '') or ''} {contact.get('phone', '') or ''}\n"
            f"Social: {social.get('twitter', '') or ''} {social.get('website', '') or ''}\n"
            + (f"AI Summary: {ai_summary}\n" if ai_summary else "")
            + f"\n=== User Question ===\n{question}"
        )
