class DriverService:
    """
    Handles logic for Drivers and DriverProfile data.
    
    This service manages listing all drivers, active drivers, create, update,
    delete profile operations.
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def list_drivers(self) -> list:
        """
        Retrieves all drivers from the database
        
        Returns:
            List[dict]: Returns drivers information
        """
        queryset = self.obj.get_queryset()
        serializer = self.obj.get_serializer(queryset, many=True)
        return serializer.data
    
    def retreive_driver_profile(self) -> dict:
        """
        Retrieves specific driver profile with id
        
        Returns:
            dict: returns driver profile data into an ReturnDict Object
        """
        profile_obj = self.obj.get_object()
        serializer = self.obj.get_serializer(profile_obj)
        return serializer.data
    
    def update_driver_profile(self, partial_flag) -> dict:
        """
        Validates request data and updates driver profile
        
        Args:
            partial_flag (bool): retrun true if update to be performed is partially\
        Returns:
            dict: returns driver profile data into an ReturnDict Object
        """
        profile_obj = self.obj.get_object()
        serializer = self.obj.get_serializer(
            profile_obj, 
            data=self.request.data, 
            partial=partial_flag
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    
    def list_active_drivers(self) -> list:
        """
        Lists all drivers with active status
        
        Returns:
            List[dict]: Returns drivers information
        """
        
        queryset = self.obj.get_queryset().filter(is_available=True).all()
        serializer = self.obj.get_serializer(queryset, many=True)
        
        return serializer.data
    
    def toggle_availability_status(self) -> dict:
        """
        Changes availability status of driver with given id
        
        Returns:
            dict: returns driver profile data into an ReturnDict Object
        """
        
        driver = self.obj.get_object()
        driver.is_available = not driver.is_available
        driver.save(update_fields=['is_available', 'updated_at'])
        serializer = self.obj.get_serializer(driver)
        
        return serializer.data 