---
adrs:
	id: 2
	title: Adoption of UV and Ruff for Dependency and Code Quality Management
	status: accepted
	date: 2025-10-01
	authors:
		- Ricardo Arias (@creep1ng)
---
# ADR 2: Adoption of UV and Ruff for Dependency and Code Quality Management

## Status
Accepted

## Context
Managing Python dependencies and enforcing code quality are critical for maintainability. The project adopts `uv` for fast, reliable dependency management and `ruff` for linting and formatting, both configured in `pyproject.toml`.

## Decision
- Use `uv` for dependency management and virtual environment handling.
- Use `ruff` for linting and code formatting.
- Configure both tools in `pyproject.toml` for consistency.
- Document usage in `docs/UV_RUFF_GUIDE.md` and the README.

## Consequences
- Faster, more reliable dependency installs.
- Consistent code style and fewer lint errors.
- Lower barrier for new contributors.

## References
- [docs/UV_RUFF_GUIDE.md]
- [pyproject.toml]
