from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from apps.users.api.v1.serializers import RegisterSerializer
from apps.common.api.exceptions import DomainError, ErrorCodes
from apps.common.utils.constants import CUSTOMER, RESTAURANT, DRIVER


class AuthService:
    """
    Handles logic for Register and login.
    
    This service manages user credentials, validation, token generation,
    and interaction with the database
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def register_user(self) -> dict:
        """
        Handles register functionalities business logic
        
        Method validates request data and registers new User with 
        specific roles
        
        Returns:
            dict: data with access and refresh token
        """
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return {
            "success": True,
            "data": serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)     
            },
            "status_code": 201,
        }
        
    def login_user(self) -> dict:
        """
        Handles login functionality business logic
        
        Method validates request data and login user and returns 
        jwt access and refresh tokens
        
        Returns:
            dict: returns data prepared for response with access and refresh tokens 
        """
        user = authenticate(
            request=self.request,
            username=self.request.data.get("username"),
            password=self.request.data.get("password")
        )
        
        if not user:
            raise DomainError(ErrorCodes.INVALID_CREDENTIALS)
        
        refresh = RefreshToken.for_user(user)
        serializer = RegisterSerializer(user)
        
        profile_id = None
        if user.role == CUSTOMER:
            profile_id = user.customer.id
        elif user.role == DRIVER:
            profile_id = user.driver.id
        elif user.role == RESTAURANT:
            profile_id = user.id
        
        return {
            "success": True,
            "data": user.username,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)     
            },
            "profile_id": profile_id,
            "role": user.role
        }
        