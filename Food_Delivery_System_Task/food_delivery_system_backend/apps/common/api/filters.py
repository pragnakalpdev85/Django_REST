import django_filters

from apps.restaurants.models import RestaurantProfile, MenuItem
from apps.orders.models import Order


class RestaurantFilters(django_filters.FilterSet):
    """
    FilterSet for the RestaurantProfile model.
    
    Provides filtering by cuisine_type (choices), is_open, delivery_fee__lte,
    minimum_order__lte, and average_rating__gte manufacturer name. Used in 
    REST API endpoints.
    """
    
    #Filters by cuisine type of restaurant
    cuisine_type = django_filters.ChoiceFilter(choices=RestaurantProfile.CUISINES)
    #filters by restaurant's open status
    is_open = django_filters.BooleanFilter()
    #filters by delivery fee is less or equal to given value
    delivery_fee__lte = django_filters.NumberFilter(field_name='delivery_fee', lookup_expr='lte')
    #filters by minimum order value is less or equal to value given
    minimum_order__lte = django_filters.NumberFilter(field_name='minimum_order', lookup_expr='lte')
    #filters by average rating is greater or equal to given value
    average_rating__gte = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    
    #Meta informations
    class Meta:
        model = RestaurantProfile
        fields = ['cuisine_type', 'is_open', 'delivery_fee__lte', 'minimum_order__lte', 'average_rating__gte']

        
class MenuItemFilters(django_filters.FilterSet):
    """
    FilterSet for the MenuItem model.
    
    Provides filtering by restaurant, category, dietary_info, is_available, price__lte.
    Used in REST API endpoints.
    """
    
    #filters menu items by restaurant
    restaurant = django_filters.CharFilter(field_name='restaurant_menuitem__name', lookup_expr='icontains')
    
    category =django_filters.ChoiceFilter(choices=MenuItem.CATEGORY)
    #filters menu items by dietary informations
    dietary_info = django_filters.ChoiceFilter(choices=MenuItem.DIETARY_INFO)
    #filters by availability status of item
    is_available = django_filters.BooleanFilter()
    #filters items price for every item which has price less or equal to given value
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    #Meta informations
    class Meta:
        model = MenuItem
        fields = ['restaurant', 'category', 'dietary_info', 'is_available', 'price__lte']   

    
class OrderFilters(django_filters.FilterSet):
    """
    FilterSet for the Order model.
    
    Provides filtering by status, restaurant, created_at_gte.Used in REST API endpoints.
    """
    
    #filters orders by restaurant name
    restaurant = django_filters.CharFilter(field_name='restaurant__name', lookup_expr='icontains')
    #filters orders by created after
    created_at_gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    #filters orders by status of the order
    status = django_filters.ChoiceFilter(choices=Order.STATUS)
    
    #Meta informations
    class Meta:
        model = Order
        fields = ['status', 'restaurant', 'created_at_gte']