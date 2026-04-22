from rest_framework.permissions import BasePermission, SAFE_METHODS
from .constants import (
    DRIVER, 
    RESTAURANT, 
    CUSTOMER
)

class IsOwnerOrReadOnly(BasePermission):
    """
    Object-Level permission
    The owner of the object can write every one else can read-only.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, "user", obj)
        return owner == request.user
    
class IsCustomer(BasePermission):
    """Allow access only to user with user role = customer"""
    
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == CUSTOMER
        )
        
class IsDriver(BasePermission):
    """Allow access only to users with role = Delivery driver"""
    
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == DRIVER
        )
        
class IsRestaurantOwner(BasePermission):
    """Allow access only to users with role = Restaurant Owner"""
    
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == RESTAURANT
        )
        
class IsProfileOwner(BasePermission):
    """
    Object-Level permission
    The user associated with a profile can edit it: other can not.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return obj.user == request.user
    