"""
Custom Domain Exceptions and Error Handlers.
"""

from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse


class SignSpeakException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class ModelNotLoadedException(SignSpeakException):
    """Raised when inference is attempted but model weights are unavailable."""

    def __init__(self, message: str = "Sign Language ML model is not loaded."):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class ResourceNotFoundException(SignSpeakException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )


async def signspeak_exception_handler(
    request: Request,
    exc: SignSpeakException
) -> JSONResponse:
    """Formats custom domain exceptions as clean JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Prevents stack trace leakage on unhandled internal errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An internal server error occurred.",
            "path": request.url.path
        }
    )
