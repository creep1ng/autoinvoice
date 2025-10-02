"""FastAPI middleware for request logging and tracking."""

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and adding request IDs."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request and add logging.

        Args:
            request: FastAPI request
            call_next: Next middleware/route handler

        Returns:
            Response from the handler
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Create a logging adapter with request ID
        log_extra = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
        }

        # Log request
        logger.info(
            f"{request.method} {request.url.path}",
            extra=log_extra,
        )

        # Process request
        start_time = time.time()
        try:
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"{request.method} {request.url.path} - {response.status_code}",
                extra={
                    **log_extra,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                },
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # Log error
            duration = time.time() - start_time
            logger.error(
                f"{request.method} {request.url.path} - ERROR",
                extra={
                    **log_extra,
                    "duration_ms": round(duration * 1000, 2),
                    "error": str(e),
                },
                exc_info=True,
            )
            raise


def get_request_id(request: Request) -> str | None:
    """
    Get request ID from request state.

    Args:
        request: FastAPI request

    Returns:
        Request ID if available
    """
    return getattr(request.state, "request_id", None)
