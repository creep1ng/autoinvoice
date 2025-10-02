---
adrs:
	id: 3
	title: Initial Dependencies Selection
	status: accepted
	date: 2025-10-01
	authors:
		- Ricardo Arias (@creep1ng)
---
# ADR 3: Initial Dependencies Selection

## Status
Accepted

## Context
The project requires a modern, robust stack for API development, PDF processing, LLM integration, and database access. The initial dependencies were chosen to support these needs and future extensibility.

## Decision
- Use FastAPI for the web API.
- Use SQLAlchemy for ORM and database access.
- Use Alembic for migrations.
- Use LangChain and langchain-openai for LLM integration.
- Use Pillow and PyMuPDF for PDF/image processing.
- Use Pydantic and pydantic-settings for data validation and configuration.
- Use psycopg for PostgreSQL connectivity.
- Use pytest and related tools for testing.

## Consequences
- The stack is modern, well-supported, and extensible.
- Easy to add new LLM providers or storage backends.
- Clear separation of concerns.

## References
- [pyproject.toml]
- [docs/v0.1.md]
