---
adrs:
	id: 5
	title: Logging Foundation
	status: accepted
	date: 2025-10-01
	authors:
		- Ricardo Arias (@creep1ng)
---
# ADR 5: Logging Foundation

## Status
Accepted

## Context
Robust logging is critical for debugging, monitoring, and observability. The project implements a logging foundation supporting both JSON and colored text formats, with integration into FastAPI and support for structured logs.

## Decision
- Implement logging configuration in `src/config/logging_config.py`.
- Provide utilities in `src/utils/logger.py`.
- Support both JSON and colored text log formats.
- Integrate logging with FastAPI middleware.
- Document logging in `docs/logging/LOGGING.md` and provide usage examples.

## Consequences
- Consistent, structured logs for all components.
- Easy integration with log aggregation tools.
- Improved developer experience and error tracking.

## References
- [src/config/logging_config.py]
- [src/utils/logger.py]
- [docs/logging/LOGGING.md]
