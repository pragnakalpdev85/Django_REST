from django.db.models import Count
from apps.restaurants.models import RestaurantProfile, Review

class RestaurantSelector:
    """
    Profile selector manages different queries for restaurant profile models.
    """
    
    @staticmethod
    def get_restaurant_profile_queryset():
        """
        Returns query for restaurant viewsets
        """
        return (
            RestaurantProfile.objects.all()
            .select_related('owner')
            .prefetch_related('restaurant_menuitem', 'restaurant_review')
            .annotate(item_count=Count('restaurant_menuitem'))
        )

    @staticmethod    
    def get_active_restaurants():
        """
        Returns queryset for all active restaurants
        """
        return (
            RestaurantProfile.objects.all()
            .select_related('owner')
            .prefetch_related('restaurant_menuitem', 'restaurant_review')
            .annotate(item_count=Count('restaurant_menuitem'))
            .filter(is_open=True)
        )

    @staticmethod    
    def get_popular_restaurants():
        """
        Returns queryset for highest rated 10 restaurants
        """
        return (
            RestaurantProfile.objects.all()
            .select_related('owner')
            .prefetch_related('restaurant_menuitem', 'restaurant_review')
            .annotate(item_count=Count('restaurant_menuitem'))
            .order_by('-average_rating')[:10]
        )

    @staticmethod    
    def get_restaurant_profile_by_user(restaurant_owner):
        """
        Returns restaurant with restaurant owner
        """
        return (
            RestaurantProfile.objects
            .select_related('owner')
            .prefetch_related('restaurant_menuitem', 'restaurant_review')
            .annotate(item_count=Count('restaurant_menuitem'))
            .filter(owner=restaurant_owner)
        )
        
    @staticmethod
    def get_restaurant_reviews(restaurant):
        """
        Returns menu of the restaurant
        """
        return (
            Review.objects
            .filter(restaurant = restaurant)
            .all()
            # .select_related('restaurant')
        )
        