"""Configuration module for AutoInvoice."""

from .logging_config import setup_logging
from .settings import get_settings, settings

__all__ = ["setup_logging", "get_settings", "settings"]
