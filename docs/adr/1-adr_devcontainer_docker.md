---
adrs:
	id: 1
	title: Devcontainer Environment and Docker Compose Orchestration
	status: accepted
	date: 2025-10-01
	authors:
		- Ricardo Arias (@creep1ng)
---
# ADR 1: Devcontainer Environment and Docker Compose Orchestration

## Status
Accepted

## Context
To ensure a consistent and reproducible development environment, the project uses a devcontainer setup. Docker Compose is used to orchestrate both the API and a Postgres database for local development and testing. This approach simplifies onboarding, reduces "works on my machine" issues, and enables parity between local and CI environments.

## Decision
- Use `.devcontainer/` with a custom `Dockerfile` and `devcontainer.json` for VS Code integration.
- Use `docker-compose.yml` to orchestrate the API service and a Postgres database.
- Provide an `.env.example` for environment variable configuration.
- Document setup and usage in the README and dedicated docs.

## Consequences
- Developers can start coding with minimal setup.
- The environment is consistent across contributors and CI.
- Docker Compose can be extended to add more services (e.g., Redis, Celery) in the future.

## References
- [docs/DEVCONTAINER.md] (to be created)
- [docker-compose.yml]
- [.devcontainer/]
