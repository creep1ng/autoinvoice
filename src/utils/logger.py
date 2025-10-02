"""Logger utility for consistent logging across modules."""

import logging
from typing import Any


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__ from calling module)

    Returns:
        Configured logger instance

    Example:
        >>> from src.utils import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing invoice", extra={"invoice_id": 123})
    """
    return logging.getLogger(name or __name__)


class LoggerMixin:
    """Mixin class to add logger property to classes."""

    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def log_with_context(
        self,
        level: int,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log with additional context.

        Args:
            level: Logging level (e.g., logging.INFO)
            message: Log message
            **kwargs: Additional context to include in log
        """
        self.logger.log(level, message, extra=kwargs)
