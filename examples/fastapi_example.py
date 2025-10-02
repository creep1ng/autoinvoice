"""Example FastAPI application with logging."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from src.api.middleware import RequestLoggingMiddleware, get_request_id
from src.config import settings, setup_logging
from src.utils import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging(settings)
    logger.info("Starting AutoInvoice API")
    yield
    # Shutdown
    logger.info("Shutting down AutoInvoice API")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)


@app.get("/")
async def root(request: Request):
    """Root endpoint."""
    request_id = get_request_id(request)
    logger.info("Root endpoint accessed", extra={"request_id": request_id})
    return {"message": "Welcome to AutoInvoice API", "request_id": request_id}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/invoices")
async def create_invoice(request: Request):
    """Create invoice endpoint."""
    request_id = get_request_id(request)

    logger.info(
        "Creating new invoice",
        extra={"request_id": request_id},
    )

    # Simulate invoice processing
    invoice_id = "INV-001"

    logger.info(
        "Invoice created successfully",
        extra={"request_id": request_id, "invoice_id": invoice_id},
    )

    return {"invoice_id": invoice_id, "status": "created"}


@app.get("/api/invoices/{invoice_id}")
async def get_invoice(invoice_id: str, request: Request):
    """Get invoice endpoint."""
    request_id = get_request_id(request)

    logger.info(
        "Retrieving invoice",
        extra={"request_id": request_id, "invoice_id": invoice_id},
    )

    return {"invoice_id": invoice_id, "status": "found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
