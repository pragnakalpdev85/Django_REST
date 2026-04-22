from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..v1.views import (
    DriverProfileViewSet,
    CustomerProfileViewSet,
    AuthLoginView,
    AuthRegisterView,
)


#registration, driver profile and customer profile urls
router = DefaultRouter()
router.register(r'drivers', DriverProfileViewSet, basename='drivers')
router.register(r'customers', CustomerProfileViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
    
    #auth urls
    path('auth/register/', AuthRegisterView.as_view(), name='register'),
    path('auth/login/', AuthLoginView.as_view(), name='login'),
    
    #obtain and refresh token urls
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]