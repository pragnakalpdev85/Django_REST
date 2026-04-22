from django.core.cache import cache

class RestaurantService:
    """
    Handles logic for restaurant profile and restaurants.
    
    This service manages create, update and retrieve operations on restaurant profile.
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def create_restaurant_profile(self):
        """
        Creates new restaurant profile
        """
        serializer = self.obj.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
    
    def update_restaurant_profile(self, partial_flag):
        """
        Updates restaurant profile data
        
        Args:
            partial_flag (bool): retrun true if update to be performed is partially
        """
        profile_object = self.obj.get_object()
        serializer = self.obj.get_serializer(
            profile_object,
            data=self.request.data,
            partial=partial_flag
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    
    def retrieve_restaurant_profile(self):
        """Retrieves driver profile by id"""
        profile_object = self.obj.get_object()
        serializer = self.obj.get_serializer(profile_object)
        
        return serializer.data  