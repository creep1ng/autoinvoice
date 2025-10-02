"""Examples of logging usage in AutoInvoice."""

from src.config import settings, setup_logging
from src.utils import get_logger
from src.utils.logger import LoggerMixin


def basic_logging_example():
    """Basic logging example."""
    # Initialize logging (do this once at app startup)
    setup_logging(settings)

    # Get logger
    logger = get_logger(__name__)

    # Different log levels
    logger.debug("Debug message - detailed information")
    logger.info("Info message - general information")
    logger.warning("Warning message - something to watch")
    logger.error("Error message - something went wrong")
    logger.critical("Critical message - serious problem")


def logging_with_context():
    """Logging with additional context."""
    logger = get_logger(__name__)

    # Log with extra context
    logger.info(
        "Processing invoice",
        extra={
            "invoice_id": "INV-001",
            "customer_id": "CUST-123",
            "amount": 1500.50,
        },
    )

    # Log exception with context
    try:
        _ = 10 / 0
    except ZeroDivisionError:
        logger.error(
            "Failed to calculate invoice total",
            extra={"invoice_id": "INV-001"},
            exc_info=True,
        )


class InvoiceProcessor(LoggerMixin):
    """Example class using LoggerMixin."""

    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id

    def process(self):
        """Process invoice with logging."""
        # Use self.logger from mixin
        self.logger.info(
            "Starting invoice processing",
            extra={"invoice_id": self.invoice_id},
        )

        try:
            # Simulate processing
            self._extract_data()
            self._validate_data()
            self._save_to_db()

            self.logger.info(
                "Invoice processed successfully",
                extra={"invoice_id": self.invoice_id},
            )

        except Exception as e:
            self.logger.error(
                "Invoice processing failed",
                extra={"invoice_id": self.invoice_id, "error": str(e)},
                exc_info=True,
            )
            raise

    def _extract_data(self):
        self.logger.debug("Extracting data from PDF")

    def _validate_data(self):
        self.logger.debug("Validating extracted data")

    def _save_to_db(self):
        self.logger.debug("Saving invoice to database")


def structured_logging_example():
    """Example with structured logging (JSON format)."""
    # To use JSON format, set LOG_FORMAT=json in .env
    logger = get_logger(__name__)

    # All these fields will be properly structured in JSON
    logger.info(
        "API request processed",
        extra={
            "request_id": "req-123",
            "user_id": "user-456",
            "endpoint": "/api/invoices",
            "method": "POST",
            "status_code": 201,
            "duration_ms": 145.23,
        },
    )


if __name__ == "__main__":
    # Run examples
    print("=== Basic Logging ===")
    basic_logging_example()

    print("\n=== Logging with Context ===")
    logging_with_context()

    print("\n=== Class with Logger Mixin ===")
    processor = InvoiceProcessor("INV-001")
    processor.process()

    print("\n=== Structured Logging ===")
    structured_logging_example()
