from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    """
    Provide custom Throttling for review creation
    """
    scope = 'review_create'
    
class OrderCreateThrottle(UserRateThrottle):
    """
    Provides custom throttling for order creation
    """
    scope = 'order_create'
    
class RegistrationRateThrottle(AnonRateThrottle):
    """
    Provides custom throttling for Registration of user
    """
    scope = 'registration'
    
class LoginRateThrottle(AnonRateThrottle):
    """
    Provides custom throttling for login user
    """
    scope = 'login'
    
    