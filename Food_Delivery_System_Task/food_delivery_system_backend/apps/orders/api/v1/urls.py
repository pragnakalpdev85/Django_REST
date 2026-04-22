from ..v1.views import OrderViewSet, CartViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

#all order routes
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'carts', CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls))
]