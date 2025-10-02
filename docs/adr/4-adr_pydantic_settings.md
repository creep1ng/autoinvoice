---
adrs:
	id: 4
	title: Pydantic-Settings for Configuration Management
	status: accepted
	date: 2025-10-01
	authors:
		- Ricardo Arias (@creep1ng)
---
# ADR 4: Pydantic-Settings for Configuration Management

## Status
Accepted

## Context
Managing configuration via environment variables is essential for 12-factor apps. The project uses `pydantic-settings` to load and validate configuration from environment variables, `.env` files, and other sources.

## Decision
- Use `pydantic-settings` for all configuration management.
- Define settings in `src/config/settings.py`.
- Provide `.env.example` for reference.
- Document configuration in `docs/SETTINGS.md`.

## Consequences
- Strongly-typed, validated configuration.
- Easy to override settings for different environments.
- Secure handling of secrets and sensitive data.

## References
- [src/config/settings.py]
- [.env.example]
- [docs/SETTINGS.md]
