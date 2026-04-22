from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MenuItemViewSet, RestaurantProfileViewSet, ReviewViewSet

#Urls for restaurans profile, menuitems and review
router = DefaultRouter()
router.register(r'restaurants', RestaurantProfileViewSet, basename='restaurants')
router.register(r'menuitems', MenuItemViewSet, basename='menuitems')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls))
]