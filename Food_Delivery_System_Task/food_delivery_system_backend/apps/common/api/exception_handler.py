from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions import DomainError
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def api_exception_handler(exc, context):
    """Global exception handler with single error format"""
    
    response = exception_handler(exc, context)
    request = context.get('request')
    
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    
        logger.error(
            f"IP: {ip} | Exception: {str(exc)} | View: {context.get('view')} | Method: {request.method if request else None} | Path: {request.path if request else None}",
            exc_info=True
        )
    
    # Domain errors (business logic)
    if isinstance(exc, DomainError):
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
    if isinstance(exc, ValidationError):
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
    return Response(
        {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong"
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )