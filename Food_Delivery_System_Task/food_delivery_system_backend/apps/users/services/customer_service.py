class CustomerService:
    """
    Handles logic for Customer profile functionalities.
    
    This service manages customer profile retrieve, update, delete operations
    and interaction with the database
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def update_profile(self, partial_flag):
        """
        Validates request data and updates profile data
        
        Args:
           partial_flag (bool): update partialy or full flag 
        """
        
        profile_obj = self.obj.get_object()
        serializer = self.obj.get_serializer(profile_obj, data=self.request.data, partial=partial_flag)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data