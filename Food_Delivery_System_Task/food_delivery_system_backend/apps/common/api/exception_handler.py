from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions import DomainError
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def log_error(message, **kwargs):
    """Safe logging with identifiers only"""
    safe_kwargs = {k: v for k, v in kwargs.items() if k not in ['password', 'token', 'secret']}
    logger.error(message, extra=safe_kwargs)

def api_exception_handler(exc, context):
    """Global exception handler with single error format"""
    
    # Domain errors (business logic)
    if isinstance(exc, DomainError):
        log_error(exc)
        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "fields": None
                }
            },
            status=exc.status_code
        )
    
    # DRF validation errors
    response = exception_handler(exc, context)
    if response is not None:
        log_error(exc)
        return Response(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input",
                    "fields": response.data
                }
            },
            status=response.status_code
        )
    
    # Unhandled exceptions (500)
    log_error(exc)
    return Response(
        {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong"
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )