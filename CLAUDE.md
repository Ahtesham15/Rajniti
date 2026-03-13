# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Rajniti** is an open-source platform for browsing and AI-enriching Indian political data (MPs and MLAs). The architecture is intentionally JSON-first: `app/data/mp.json` and `app/data/mla.json` are the source of truth — no SQL database for politicians. The backend is Flask (Python), the frontend is Next.js (TypeScript), and LangChain agents enrich politician profiles via free-tier LLMs.

## Commands

### Backend

```bash
make install          # Create venv + install deps
make install-dev      # Include test dependencies
make run              # Start Flask API on :8000
make lint-backend     # Black + isort + Flake8 + mypy
make format           # Auto-format with Black + isort
make test             # All tests
make test-unit        # Unit tests only
make test-e2e         # End-to-end tests
make coverage         # Tests + coverage report

# Docker (local dev with Postgres)
make dev              # docker-compose up (Postgres + API)

# Database
make db-migrate       # Run Alembic migrations
make db-reset         # Reset database (destructive)
```

Run a single test:
```bash
source venv/bin/activate
pytest tests/unit/test_specific.py -v
pytest tests/unit/test_specific.py::TestClass::test_method -v
```

### Frontend

```bash
cd frontend
npm run dev           # Dev server
npm run build         # Production build
npm run lint          # ESLint + TypeScript check
npm test              # Jest unit tests
npm run test:watch    # Watch mode
npm run test:coverage # Coverage report
```

### Agents (CLI enrichment)

```bash
source venv/bin/activate
python scripts/run_politician_agent.py --name "Politician Name"
python scripts/sync_chroma_politicians.py  # Populate vector DB
```

## Architecture

### Data Flow

```
Frontend (Next.js) → Flask API → JSON files (app/data/)
                              → ChromaDB (vector search)
                              → PostgreSQL (users only)
```

Politician data lives entirely in JSON. The `User` table (PostgreSQL via SQLAlchemy/Alembic) is the only SQL model.

### Backend Layer Structure

`Routes (Flask blueprints)` → `Controllers` → `Services` → `JSON files`

- `app/routes/` — Flask blueprints (`api_routes.py`, `user_routes.py`)
- `app/controllers/` — Thin request handlers
- `app/services/` — Business logic (`politician_service.py` reads JSON; `vector_db_service.py`; `questions_service.py`; `llm_cache.py`)
- `app/agents/` — LangChain enrichment agents (PoliticianAgent with sub-processes per topic: education, family, crimes, political background)
- `app/config/free_tier_llm.py` — LLM failover: Gemini → Groq → OpenAI → Perplexity with per-model cooldown on rate limits
- `app/tools/` — Agent tools (web scraper, Wikipedia, web search via DDGS)
- `app/prompts/` — LLM prompt builders
- `app/core/` — Utilities (caching, logging, exceptions, vector DB, response formatting)

### Frontend Structure

Next.js App Router under `frontend/app/`:
- `api/` — API route handlers (NextAuth callbacks)
- `politician/` — Politician detail pages
- `dashboard/` — Stats dashboard
- `onboarding/` — Contributor onboarding
- `contributors/` — Contributors display

Auth: NextAuth.js with Google OAuth. Backend syncs user data.

### Adding a New Enrichment Process

1. Create a process class in `app/agents/` inheriting from the base agent pattern
2. Register it in `PoliticianAgent`
3. Add corresponding prompt builder in `app/prompts/politician_prompts.py`
4. The result is written back to the JSON file

### LLM Configuration

At least one API key is required in `.env`:
- `GEMINI_API_KEY` — Recommended (generous free tier)
- `GROQ_API_KEY` — Fast fallback
- `OPENAI_API_KEY` or `PERPLEXITY_API_KEY` — Further fallbacks

### Environment Setup

Copy `.env.example` to `.env`. Key variables:
- `DATABASE_URL` — PostgreSQL connection string
- `NEXT_PUBLIC_API_URL` — Backend URL for frontend (default: `http://localhost:8000`)
- LLM API keys (above)

### Testing Strategy

- **Unit tests** (`tests/unit/`) — Fast, isolated, use SQLite (`TESTING=true`)
- **Integration tests** (`tests/integration/`) — May use real services
- **E2E tests** (`tests/e2e/`) — Full system
- Coverage minimum: 60%
- Frontend tests: Jest + React Testing Library in `frontend/`

### CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on push/PR to `production`/`development`:
- Parallel: backend lint, unit/integration/E2E tests, frontend lint/tests/build, security scan (Safety + Bandit), Docker build test
- All jobs must pass before merge

### Data Contributions (PRs)

PRs that add/update politician data should only modify JSON files (`app/data/mp.json` or `app/data/mla.json`). The `cache.db` file must never be committed.
