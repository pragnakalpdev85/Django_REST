from apps.restaurants.models import MenuItem, Review

class MenuItemSelector:
    """
    MenuItem selector manages different queries for MenuItem models.
    """
    
    @staticmethod
    def get_menuitem_queryset():
        """
        Returns query set of the menu item
        """
        return (
            MenuItem.objects.all()
            .select_related('restaurant')
            .prefetch_related('menuitem_reviews')
        )   
    
    def get_reviews_of_menuitem(menu_item):
        """
        Returns queryset of reviews filtered by menu item
        """
        
        return (
            Review.objects.
            filter(menu_item = menu_item)
            .all()
            .select_related('menu_item')
        )
        