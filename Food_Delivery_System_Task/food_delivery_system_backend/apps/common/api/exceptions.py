class DomainError(Exception):
    """Base class for all business logic errors"""
    code = "DOMAIN_ERROR"
    status_code = 400
    
    def __init__(self, message=None):
        self.message = message or self.__class__.__name__.replace('_', ' ').title()
        super().__init__(self.message)
        

class ErrorCodes:
    # Authentication & Authorization
    AUTH_REQUIRED = "AUTH_REQUIRED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    
    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_FIELD = "MISSING_FIELD"
    
    # Resources
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    ARTICLE_NOT_FOUND = "ARTICLE_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    
    # Business Logic
    DRIVER_NOT_AVAILABLE = "DRIVER_NOT_AVAILABLE"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"
    CANNOT_CANCEL_ORDER = "CANNOT_CANCEL_ORDER"
    CANNOT_UPDATE_ORDER_STATUS = "CANNOT_UPDATE_ORDER_STATUS"
    CART_DOES_NOT_EXISTS = "CART_DOES_NOT_EXISTS"
    ORDER_ITEM_DOES_NOT_EXISTS = "ORDER_ITEM_DOES_NOT_EXISTS"
    
    # Rate Limiting
    RATE_LIMITED = "RATE_LIMITED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    
    # Server Errors
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"