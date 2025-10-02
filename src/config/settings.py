"""Application settings using pydantic-settings.

This module provides a centralized configuration system that automatically
loads settings from environment variables and .env files. All settings are
type-validated using Pydantic.

Basic Usage:
    >>> from src.config import settings
    >>> print(settings.app_name)
    'AutoInvoice'
    >>> print(settings.database_url)
    'postgresql+psycopg://user:pass@host:5432/db'

Environment Configuration:
    Settings can be configured via:
    1. Environment variables (highest priority)
    2. .env file in project root
    3. Default values (lowest priority)

    Example .env file:
        DEBUG=true
        LOG_LEVEL=DEBUG
        POSTGRES_HOST=localhost
        OPENAI_API_KEY=sk-your-key-here

For complete documentation, see: docs/settings/SETTINGS.md
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class uses Pydantic's BaseSettings to automatically load configuration
    from environment variables and .env files. All fields are type-validated.

    Attributes:
        app_name: Application name
        app_version: Application version
        debug: Enable debug mode (affects logging, timeouts, etc.)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log output format ('text' or 'json')
        log_file: Path to log file (None disables file logging)
        log_file_max_bytes: Maximum log file size before rotation
        log_file_backup_count: Number of rotated log files to keep
        postgres_host: PostgreSQL server hostname
        postgres_port: PostgreSQL server port
        postgres_user: PostgreSQL username
        postgres_password: PostgreSQL password
        postgres_db: PostgreSQL database name
        openai_api_key: OpenAI API key for LLM operations
        openai_model: OpenAI model name to use

    Properties:
        database_url: Complete PostgreSQL connection URL (computed)
        project_root: Project root directory path (computed)
        logs_dir: Logs directory path (computed, auto-created)

    Example:
        >>> from src.config import settings
        >>> # Access settings
        >>> settings.log_level
        'INFO'
        >>> # Use computed properties
        >>> settings.database_url
        'postgresql+psycopg://user:pass@localhost:5432/autoinvoice'
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # Load from .env file if present
        env_file_encoding="utf-8",  # Use UTF-8 encoding for .env file
        case_sensitive=False,  # Allow LOG_LEVEL or log_level
        extra="ignore",  # Ignore unknown environment variables
    )

    # ============================================================================
    # Application Settings
    # ============================================================================

    app_name: str = "AutoInvoice"
    """Application name used in API documentation and logs."""

    app_version: str = "0.1.0"
    """Application version following semantic versioning."""

    debug: bool = Field(
        default=False,
        description="Enable debug mode (affects logging, error messages, timeouts)",
    )
    """Enable debug mode for development (use DEBUG=true in environment)."""

    # ============================================================================
    # Logging Settings
    # ============================================================================

    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    """Minimum logging level. Use LOG_LEVEL=DEBUG for verbose logs."""

    log_format: str = Field(
        default="text",
        description="Log format: 'text' (colored console) or 'json' (structured)",
    )
    """Log output format. Use 'text' for development, 'json' for production."""

    log_file: str | None = Field(
        default=None,
        description="Log file path (None disables file logging)",
    )
    """
    Optional log file path. If set, logs are written to this file with rotation.
    Example: LOG_FILE=logs/autoinvoice.log
    """

    log_file_max_bytes: int = Field(
        default=10_485_760,  # 10MB
        description="Maximum log file size in bytes before rotation",
    )
    """Maximum size of log file before rotation (default: 10MB)."""

    log_file_backup_count: int = Field(
        default=5,
        description="Number of rotated backup log files to keep",
    )
    """Number of backup log files to retain (e.g., app.log.1, app.log.2, ...)."""

    # ============================================================================
    # Database Settings
    # ============================================================================

    postgres_host: str = Field(default="localhost")
    """PostgreSQL server hostname or IP address."""

    postgres_port: int = Field(default=5432)
    """PostgreSQL server port number."""

    postgres_user: str = Field(default="autoinvoice")
    """PostgreSQL username for authentication."""

    postgres_password: str = Field(default="autoinvoice")
    """PostgreSQL password for authentication. Use env var in production!"""

    postgres_db: str = Field(default="autoinvoice")
    """PostgreSQL database name to connect to."""

    @property
    def database_url(self) -> str:
        """Construct complete PostgreSQL connection URL.

        Returns:
            SQLAlchemy-compatible database URL using psycopg driver.

        Example:
            >>> settings.database_url
            'postgresql+psycopg://user:pass@localhost:5432/autoinvoice'
        """
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ============================================================================
    # OpenAI / LLM Settings
    # ============================================================================

    openai_api_key: str | None = Field(default=None)
    """
    OpenAI API key for LLM operations. Required for invoice extraction.
    Set via: OPENAI_API_KEY=sk-your-key-here
    """

    openai_model: str = Field(default="gpt-4o-mini")
    """
    OpenAI model to use for LLM operations.
    Options: gpt-4o-mini, gpt-4o, gpt-4-turbo, etc.
    """

    # ============================================================================
    # Computed Path Properties
    # ============================================================================

    @property
    def project_root(self) -> Path:
        """Get absolute path to project root directory.

        Returns:
            Path to the workspace root directory.

        Example:
            >>> settings.project_root
            PosixPath('/workspace')
        """
        return Path(__file__).parent.parent.parent

    @property
    def logs_dir(self) -> Path:
        """Get absolute path to logs directory (auto-creates if missing).

        The logs directory is created automatically if it doesn't exist.

        Returns:
            Path to the logs directory.

        Example:
            >>> settings.logs_dir
            PosixPath('/workspace/logs')
        """
        logs_path = self.project_root / "logs"
        logs_path.mkdir(exist_ok=True)
        return logs_path


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern).

    This function returns a cached instance of the Settings class, ensuring
    that settings are loaded only once and reused throughout the application.

    Returns:
        Cached Settings instance.

    Example:
        >>> from src.config import get_settings
        >>> settings1 = get_settings()
        >>> settings2 = get_settings()
        >>> settings1 is settings2  # Same instance
        True

    Note:
        For testing, you can clear the cache:
        >>> get_settings.cache_clear()
    """
    return Settings()


# Global settings instance (recommended for most use cases)
settings = get_settings()
"""
Global settings instance for convenient access.

This is a cached singleton instance that can be imported and used directly:

    >>> from src.config import settings
    >>> print(settings.log_level)
    'INFO'

For more control (e.g., in tests), use get_settings() instead.
"""
