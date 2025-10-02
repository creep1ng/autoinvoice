"""Quick Start: Add Logging to Your AutoInvoice Code

This file shows how to quickly add logging to your existing code.
"""

# ============================================================================
# STEP 1: Initialize Logging (Do this ONCE at application startup)
# ============================================================================

# In your main.py or app.py:
from src.config import settings, setup_logging

# Initialize logging
setup_logging(settings)


# ============================================================================
# STEP 2: Add Logger to Any Module
# ============================================================================

# At the top of any Python file:
from src.utils import get_logger

# Get logger instance
logger = get_logger(__name__)


# ============================================================================
# STEP 3: Use Logging Throughout Your Code
# ============================================================================

def process_invoice(invoice_path: str):
    """Example function with logging."""
    # Log function entry
    logger.info(f"Processing invoice from {invoice_path}")

    try:
        # Your code here
        invoice_data = extract_invoice_data(invoice_path)

        # Log successful operation with context
        logger.info(
            "Invoice extracted successfully",
            extra={
                "invoice_id": invoice_data.get("id"),
                "amount": invoice_data.get("total"),
                "items_count": len(invoice_data.get("items", [])),
            }
        )

        return invoice_data

    except FileNotFoundError:
        # Log specific error
        logger.error(f"Invoice file not found: {invoice_path}")
        raise

    except Exception:
        # Log unexpected error with full traceback
        logger.error(
            "Failed to process invoice",
            extra={"invoice_path": invoice_path},
            exc_info=True  # This includes the full stack trace
        )
        raise


# ============================================================================
# STEP 4: Use in Classes
# ============================================================================

# Option A: Using LoggerMixin (recommended)
from src.utils.logger import LoggerMixin


class InvoiceService(LoggerMixin):
    """Service class with automatic logger."""

    def __init__(self, db_connection):
        self.db = db_connection

    def save_invoice(self, invoice_data: dict):
        # self.logger is automatically available
        self.logger.info(
            "Saving invoice to database",
            extra={"invoice_id": invoice_data.get("id")}
        )

        try:
            self.db.save(invoice_data)
            self.logger.info("Invoice saved successfully")
        except Exception:
            self.logger.error(
                "Failed to save invoice",
                exc_info=True
            )
            raise


# Option B: Manual logger (if you don't want to use mixin)
class InvoiceValidator:
    """Validator class with manual logger."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def validate(self, invoice_data: dict):
        self.logger.debug("Starting invoice validation")

        if not invoice_data.get("total"):
            self.logger.warning("Invoice missing total amount")
            return False

        self.logger.info("Invoice validation passed")
        return True


# ============================================================================
# STEP 5: FastAPI Integration
# ============================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.middleware import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan with logging initialization."""
    # Startup
    setup_logging(settings)
    logger.info("Application starting")
    yield
    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(lifespan=lifespan)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)


@app.post("/api/invoices")
async def create_invoice(invoice_data: dict):
    """API endpoint with logging."""
    logger.info(
        "Creating new invoice",
        extra={
            "customer_id": invoice_data.get("customer_id"),
            "amount": invoice_data.get("amount"),
        }
    )

    try:
        # Process invoice
        result = process_invoice_data(invoice_data)

        logger.info(
            "Invoice created successfully",
            extra={"invoice_id": result.get("id")}
        )

        return {"status": "success", "invoice_id": result.get("id")}

    except Exception as e:
        logger.error(
            "Failed to create invoice",
            extra={"error": str(e)},
            exc_info=True
        )
        raise


# ============================================================================
# STEP 6: Common Logging Patterns
# ============================================================================

def common_patterns():
    """Common logging patterns you'll use."""

    # 1. Simple message
    logger.info("User logged in")

    # 2. Message with variables
    user_id = "user123"
    logger.info(f"User {user_id} logged in")

    # 3. Message with structured context (PREFERRED)
    logger.info(
        "User logged in",
        extra={"user_id": user_id, "ip_address": "192.168.1.1"}
    )

    # 4. Different log levels
    logger.debug("Detailed debugging info")
    logger.info("General information")
    logger.warning("Something unexpected")
    logger.error("An error occurred")
    logger.critical("Critical system failure")

    # 5. Exception logging
    try:
        risky_operation()
    except Exception:
        logger.error("Operation failed", exc_info=True)

    # 6. Conditional logging
    if user_is_admin:
        logger.warning(
            "Admin action performed",
            extra={"action": "delete_user", "target": "user123"}
        )

    # 7. Performance logging
    import time
    start_time = time.time()
    perform_operation()
    duration = time.time() - start_time

    logger.info(
        "Operation completed",
        extra={"duration_ms": round(duration * 1000, 2)}
    )


# ============================================================================
# STEP 7: Configuration (Optional)
# ============================================================================

# Create/edit .env file in project root:
"""
# Development
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Production
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/autoinvoice.log
"""

# ============================================================================
# That's it! You're ready to use logging in your AutoInvoice project.
# ============================================================================

# For more details, see:
# - docs/logging/LOGGING.md - Complete documentation
# - examples/logging_examples.py - Working examples
# - examples/fastapi_example.py - FastAPI integration
