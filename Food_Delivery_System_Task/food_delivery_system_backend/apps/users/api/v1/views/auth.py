from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny 
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

from apps.common.utils.custom_responses import success_response

from apps.users.services import AuthService
from apps.users.api.v1.serializers import RegisterSerializer
from apps.common.api.throttle import LoginRateThrottle, RegistrationRateThrottle


class AuthRegisterView(APIView):
    """
    POST /api/v1/auth/register/
    Registers a new user with role.
    """
    permission_classes = [AllowAny]
    throttle_classes = [RegistrationRateThrottle]
    
    @extend_schema(
        summary="Registers an user",
        description="Create a new user account with user roles",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="User Created, Token generated."),
            400: OpenApiResponse(description="Invalid Input data / Validation Error"),
        },
        tags=["Authentication"]
    )
    def post(self, request):
        """
        Post method for Register API View
        """
        service = AuthService(view_object=self, request_object=request)
        obj = service.register_user()
        return Response(
            obj, 
            status=status.HTTP_201_CREATED
        )
        

class AuthLoginView(APIView):
    """
    POST /api/v1/auth/login/
    Login a user and returns tokens
    """
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    @extend_schema(
        summary="Login an user",
        description="Login user account with user roles and generate access token",
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "username": serializers.CharField(help_text="User username"),
                "password": serializers.CharField(help_text="User password")
            },
        ),
        responses={
            200: OpenApiResponse(description="User Loged in, Token generated."),
            400: OpenApiResponse(description="Invalid Input data / Validation Error"),
        },
        tags=["Authentication"]
    )
    def post(self, request):
        """
        Post method for Login API View
        """
        service = AuthService(view_object=self, request_object=request)
        obj = service.login_user()
        return Response(
            obj,
            status=status.HTTP_200_OK
        )