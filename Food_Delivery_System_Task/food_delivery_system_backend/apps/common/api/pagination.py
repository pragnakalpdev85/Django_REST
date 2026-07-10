from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination

class RestaurantPageNumberPagination(PageNumberPagination):
    """
    Custom PageNumberPagination to handle specific QuerySet slicing for restaurant's data.

    This class extends the PageNumberPagination to provide 
    additional metadata for returning restaurants data.

    Attributes:
        page_size (int): The number of items to display on each page.
    """
    
    page_size = 20
    
class CustomerProfilePageNumberPagination(PageNumberPagination):
    """
    Custom PageNumberPagination to handle specific QuerySet slicing for restaurant's data.

    This class extends the PageNumberPagination to provide 
    additional metadata for returning restaurants data.

    Attributes:
        page_size (int): The number of items to display on each page.
    """
    
    page_size = 20

    
class MenuItemPageNumberPagination(PageNumberPagination):
    """
    Custom PageNumberPagination to handle specific QuerySet slicing for menu items.

    This class extends the PageNumberPagination to provide 
    additional metadata for returning menu items.

    Attributes:
        page_size (int): The number of items to display on each page.
    """
    
    page_size = 30

    
class OrdersCursorPagination(PageNumberPagination):
    """
    Custom CursorPagination to handle specific QuerySet slicing for orders.

    This class extends the CursorPagination to provide 
    additional metadata for returning orders.

    Attributes:
        page_size (int): The number of items to display on each page.
        ordering (str): default ordering for orders data
    """
    
    page_size = 10
    ordering = '-created_at'
    
    
class ReviewLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom LimitOffsetPagination to handle specific QuerySet slicing for reviews.

    This class extends the LimitOffsetPagination to provide 
    additional metadata for returning orders.

    Attributes:
        default_limit (int): Default number of records if limit is not specified
        limit_query_param (str): URL parameter name for limit
        offset_query_param (str): URL parameter name for offset
        max_limit (int): Maximum limit allowed for records
    """
    
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50