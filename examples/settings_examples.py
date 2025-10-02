"""Example: Using Settings in AutoInvoice

This file demonstrates how to use the Settings system in your code.
"""

from pathlib import Path

from src.config import get_settings, settings


def example_basic_usage():
    """Basic usage of settings."""
    print("=== Basic Settings Usage ===\n")

    # Access global settings instance (recommended for most cases)
    print(f"App Name: {settings.app_name}")
    print(f"App Version: {settings.app_version}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Log Level: {settings.log_level}")
    print(f"Log Format: {settings.log_format}")


def example_database_settings():
    """Using database settings."""
    print("\n=== Database Settings ===\n")

    # Access individual database settings
    print(f"Database Host: {settings.postgres_host}")
    print(f"Database Port: {settings.postgres_port}")
    print(f"Database Name: {settings.postgres_db}")
    print(f"Database User: {settings.postgres_user}")

    # Use computed database URL property
    print(f"\nDatabase URL: {settings.database_url}")

    # Example: Create SQLAlchemy engine
    # from sqlalchemy import create_engine
    # engine = create_engine(settings.database_url)


def example_openai_settings():
    """Using OpenAI settings."""
    print("\n=== OpenAI Settings ===\n")

    if settings.openai_api_key:
        # Mask the key for display
        masked_key = f"{settings.openai_api_key[:10]}...{settings.openai_api_key[-4:]}"
        print(f"OpenAI API Key: {masked_key}")
    else:
        print("OpenAI API Key: Not configured")

    print(f"OpenAI Model: {settings.openai_model}")

    # Example: Create LangChain LLM
    # from langchain_openai import ChatOpenAI
    # llm = ChatOpenAI(
    #     api_key=settings.openai_api_key,
    #     model=settings.openai_model,
    # )


def example_path_properties():
    """Using path properties."""
    print("\n=== Path Properties ===\n")

    # Access computed path properties
    print(f"Project Root: {settings.project_root}")
    print(f"Logs Directory: {settings.logs_dir}")

    # Use paths in your code
    uploads_dir = settings.project_root / "uploads"
    print(f"Uploads Directory: {uploads_dir}")

    # Create directories as needed
    uploads_dir.mkdir(exist_ok=True)
    print(f"Uploads directory exists: {uploads_dir.exists()}")


def example_get_settings_function():
    """Using get_settings() function."""
    print("\n=== get_settings() Function ===\n")

    # Get settings instance (cached singleton)
    settings1 = get_settings()
    settings2 = get_settings()

    # Both return the same instance
    print(f"Same instance: {settings1 is settings2}")
    print(f"Settings ID 1: {id(settings1)}")
    print(f"Settings ID 2: {id(settings2)}")


def example_in_class():
    """Using settings in a class."""
    print("\n=== Settings in Classes ===\n")

    class InvoiceProcessor:
        """Example service class using settings."""

        def __init__(self):
            # Access settings in __init__
            self.max_retries = 3
            self.debug = settings.debug

        def process(self, invoice_path: Path) -> dict:
            """Process invoice with settings-based behavior."""
            print(f"Processing invoice: {invoice_path}")

            # Use settings to control behavior
            if self.debug:
                print("  [DEBUG] Detailed processing info...")

            # Simulate processing
            result = {
                "status": "success",
                "invoice_id": "INV-001",
                "debug_mode": self.debug,
            }

            return result

    # Use the class
    processor = InvoiceProcessor()
    result = processor.process(Path("invoice.pdf"))
    print(f"Result: {result}")


def example_conditional_behavior():
    """Conditional behavior based on settings."""
    print("\n=== Conditional Behavior ===\n")

    # Different behavior in debug vs production
    if settings.debug:
        print("Running in DEBUG mode:")
        print("  - Verbose logging enabled")
        print("  - Detailed error messages")
        print("  - Longer timeouts")
        timeout = 60
        retries = 1
    else:
        print("Running in PRODUCTION mode:")
        print("  - Minimal logging")
        print("  - Generic error messages")
        print("  - Standard timeouts")
        timeout = 10
        retries = 3

    print(f"\nConfiguration: timeout={timeout}s, retries={retries}")


def example_fastapi_integration():
    """Example FastAPI integration with settings."""
    print("\n=== FastAPI Integration Example ===\n")

    # This shows how you would use settings in FastAPI
    print("Example FastAPI code:")
    print("""
    from fastapi import FastAPI
    from src.config import settings, setup_logging

    # Initialize logging
    setup_logging(settings)

    # Create app with settings
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    @app.get("/config")
    async def get_config():
        return {
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
        }
    """)


def example_environment_based():
    """Show environment-based configuration."""
    print("\n=== Environment-Based Configuration ===\n")

    print("Settings are loaded from (in order):")
    print("1. Environment variables")
    print("2. .env file")
    print("3. Default values")
    print("\nCurrent configuration source:")

    import os

    # Check if using environment variables or defaults
    log_level_source = "environment" if "LOG_LEVEL" in os.environ else "default"
    debug_source = "environment" if "DEBUG" in os.environ else "default"

    print(f"  LOG_LEVEL: {settings.log_level} (from {log_level_source})")
    print(f"  DEBUG: {settings.debug} (from {debug_source})")

    print("\nTo override settings:")
    print("  export LOG_LEVEL=DEBUG")
    print("  export DEBUG=true")


def example_all_settings():
    """Display all available settings."""
    print("\n=== All Available Settings ===\n")

    print("Application:")
    print(f"  app_name: {settings.app_name}")
    print(f"  app_version: {settings.app_version}")
    print(f"  debug: {settings.debug}")

    print("\nLogging:")
    print(f"  log_level: {settings.log_level}")
    print(f"  log_format: {settings.log_format}")
    print(f"  log_file: {settings.log_file}")
    print(f"  log_file_max_bytes: {settings.log_file_max_bytes:,}")
    print(f"  log_file_backup_count: {settings.log_file_backup_count}")

    print("\nDatabase:")
    print(f"  postgres_host: {settings.postgres_host}")
    print(f"  postgres_port: {settings.postgres_port}")
    print(f"  postgres_user: {settings.postgres_user}")
    print(f"  postgres_password: {'*' * len(settings.postgres_password)}")
    print(f"  postgres_db: {settings.postgres_db}")
    print(f"  database_url: {settings.database_url.split('@')[0]}@***")

    print("\nOpenAI:")
    if settings.openai_api_key:
        masked = f"{settings.openai_api_key[:7]}...{settings.openai_api_key[-4:]}"
        print(f"  openai_api_key: {masked}")
    else:
        print("  openai_api_key: Not set")
    print(f"  openai_model: {settings.openai_model}")

    print("\nPaths:")
    print(f"  project_root: {settings.project_root}")
    print(f"  logs_dir: {settings.logs_dir}")


if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_database_settings()
    example_openai_settings()
    example_path_properties()
    example_get_settings_function()
    example_in_class()
    example_conditional_behavior()
    example_fastapi_integration()
    example_environment_based()
    example_all_settings()

    print("\n" + "=" * 60)
    print("For more information, see: docs/settings/SETTINGS.md")
    print("=" * 60)
