class MenuItemService:
    """
    Handles logic for menu item.
    
    This service manages create, update, retrieve, and availability toggle operations on 
    menu items.
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def create_menuitem(self):
        """
        Creates new menu item
        """
        serializer = self.obj.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
        
    def retrieve_menuitem(self):
        """
        Retrieves a menu item
        """
        menuitem = self.obj.get_object()
        serializer = self.obj.get_serializer(menuitem)
        return serializer.data
    
    def update_menuitem(self, partial_flag):
        """
        Updates menu items partially or whole menuitem
        """
        menuitem = self.obj.get_object()
        serializer = self.obj.get_serializer(
            menuitem, 
            data=self.request.data, 
            partial=partial_flag
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
    
    def toggle_availability_status(self):
        """
        Toggles availability status of the menu item
        """
        menuitem = self.obj.get_object()
        menuitem.is_available = not menuitem.is_available
        menuitem.save(update_fields=['is_available', 'updated_at'])
        
        serializer = self.obj.get_serializer(menuitem)
        
        return serializer.data
        
        
        