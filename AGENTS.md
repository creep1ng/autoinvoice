# AGENTS.md — AI Coding Agent Guide for Autoinvoice

## Project Overview
- **Autoinvoice** is a modular, SOLID-architecture Python project for extracting invoice data from PDFs using LLMs (OpenAI via LangChain).
- The codebase is organized for separation of concerns: API, business logic, configuration, utilities, and documentation are all clearly separated.

## Key Architecture & Data Flow
- **API Layer:**
  - FastAPI endpoints in `src/api/` (see `middleware.py` for logging integration).
  - Main endpoint: `/upload` (POST, accepts PDF, returns extracted invoice data).
- **Business Logic:**
  - PDF processing, OCR, and extraction in `src/services/`.
  - LLM connectors (planned: `core/extractors/` per v0.1 spec).
- **Configuration:**
  - All settings via `src/config/settings.py` (uses `pydantic-settings`).
  - Logging config in `src/config/logging_config.py`.
- **Utilities:**
  - Logging helpers in `src/utils/logger.py`.
- **Documentation:**
  - Component docs in `docs/logging/`, `docs/settings/`, and ADRs in `docs/adr/`.

## Developer Workflows
- **Environment:**
  - Use the devcontainer (`.devcontainer/`) and `docker-compose.yml` for local development (API + Postgres).
  - Copy `.env.example` to `.env` and adjust as needed.
- **Dependency Management:**
  - Use `uv` for installing dependencies (`uv pip install ...`).
  - Lint/format with `ruff` (configured in `pyproject.toml`).
- **Testing:**
  - Run tests with `pytest` (see `[tool.pytest.ini_options]` in `pyproject.toml`).
  - Coverage: `pytest --cov=src` (HTML report in `htmlcov/`).
- **Logging:**
  - Logging is structured (JSON/text), see `docs/logging/LOGGING.md` and `src/config/logging_config.py`.
- **Settings:**
  - All config via environment or `.env` file, documented in `docs/settings/SETTINGS.md`.

## Project Conventions & Patterns
- **Strict separation:** No business logic in API layer; use services and utils.
- **Settings:** Always use the `Settings` class from `src/config/settings.py` for config.
- **Logging:** Use logger from `src/utils/logger.py` or the provided mixin.
- **Testing:** Place all tests in `tests/` (not yet present in this branch, but see `pyproject.toml`).
- **Documentation:**
  - Add new ADRs in `docs/adr/` using the template.
  - Component docs go in `docs/logging/`, `docs/settings/`, etc.
- **Examples:**
  - See `examples/` for usage patterns (e.g., `logging_examples.py`, `settings_examples.py`).

## Branching & Commit Conventions
- Branches must follow `{issue-number}-{category}/{short-title}` (see `CONTRIBUTING.md`).
- Commit messages must follow the conventional format described in `CONTRIBUTING.md`.
- Categories and workflow should match `.github/ISSUE_TEMPLATE` and PR templates.

## Integration Points
- **LLM Extraction:**
  - Uses LangChain and OpenAI (see dependencies in `pyproject.toml`).
  - Future extractors should be added under `src/services/` or `core/extractors/` (per v0.1 plan).
- **Database:**
  - Postgres via SQLAlchemy and Alembic (see dependencies).

## References
- [README.md](README.md)
- [docs/v0.1.md](docs/v0.1.md)
- [docs/logging/LOGGING.md](docs/logging/LOGGING.md)
- [docs/settings/SETTINGS.md](docs/settings/SETTINGS.md)
- [docs/adr/index.md](docs/adr/index.md)

---
If you are an AI agent, follow these conventions and reference the above files for implementation details. For new features, check ADRs and component docs before coding.
