from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.common.api.filters import MenuItemFilters
from apps.restaurants.services import MenuItemService
from apps.common.utils.permissions import IsRestaurantOwner, IsOwnerOrReadOnly
from apps.restaurants.selectors import MenuItemSelector
from apps.common.utils.custom_responses import success_response
from apps.common.api.pagination import MenuItemPageNumberPagination
from ..serializers import MenuItemSerializer, MenuItemCreateUpdateSerializer, ReviewSerializer


@extend_schema_view(
    partial_update = extend_schema(
        summary="Updates menu item",
        description="Updates individual menu item partially or whole menu item",
        responses={
            200: MenuItemCreateUpdateSerializer,
            404: OpenApiResponse(description="MenuItem not found")  
        },
        tags=['MenuItem']
    )  
)
class MenuItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows menu items to be viewed or edited.
    
    list: Return a list of all existing menuitems with restaurant info.
    create: Create a new menu item.
    retrieve: Return the menu item given by ID.
    update: Update all fields of menu item with a specific id.
    partial_update: Update only specified fields of a specific menu item.
    destroy: Delete a menu item instance.
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MenuItemFilters
    pagination_class = MenuItemPageNumberPagination

    search_fields = ['name', 'restaurant__name', 'description', 'category', 'dietary_info']
    ordering_fields = ['menuitem_reviews__rating', 'created_at', 'price']
    
    
    def get_queryset(self):
        """
        Returns queryset for view
        """
        
        return MenuItemSelector.get_menuitem_queryset()
    

    def get_serializer_class(self):
        """
        Returns serializer class based on current action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return MenuItemCreateUpdateSerializer
        
        return MenuItemSerializer
    
    
    def get_permissions(self):
        """
        Returns permission classes based on current action
        """
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            return [IsRestaurantOwner()]
        
        return [AllowAny()]
    
    
    def get_object(self):
        """
        checks permission at object level and returns object
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        
        return obj
    
        
    @extend_schema(
        summary="Creates new menuitem",
        description="Creates new menu item",
        responses={
            201: MenuItemCreateUpdateSerializer,
            400: OpenApiResponse(description="Invalid input / Validation error")
        },
        tags=['MenuItem']
    )
    def create(self, request, *args, **kwargs):
        """Handles POST request to create new menu item"""
        service = MenuItemService(view_object=self, request_object=request)
        data = service.create_menuitem()
        return success_response(
            message="Menu item created successfully",
            data=data,
            status_code=status.HTTP_201_CREATED   
        )
    
    
    @extend_schema(
        summary="List of all menu items",
        description="Retrieve list of all menu items",
        responses={
            200: MenuItemSerializer  
        },
        tags=['MenuItem']
    )
    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to list of menu items.
        """
        queryset = self.filter_queryset(self.get_queryset().order_by('restaurant_id'))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return success_response(
                message="List of menu items retrieved successfully",
                data=paginated_data, 
                status_code=status.HTTP_200_OK
            )
            
        items = self.get_serializer(queryset, many=True)
        return success_response(
            message="List of menu items retrieved successfully",
            data=items.data, 
            status_code=status.HTTP_200_OK
        )
      
      
    @extend_schema(
        summary="Retrieves menu item",
        description="Retrieves individual menu item",
        responses={
            200: MenuItemSerializer,
            404: OpenApiResponse(description="MenuItem not found")  
        },
        tags=['MenuItem']
    )  
    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve data of a menu item 
        with id.
        """
        service = MenuItemService(view_object=self, request_object=request)
        data = service.retrieve_menuitem()
        return success_response(
            message = "Menu item retrieved successfully",
            data = data,
            status_code = status.HTTP_200_OK
        )
      
    
    @extend_schema(
        summary="Updates menu item",
        description="Updates individual menu item partially or whole menu item",
        responses={
            200: MenuItemCreateUpdateSerializer,
            404: OpenApiResponse(description="MenuItem not found")  
        },
        tags=['MenuItem']
    )  
    def update(self, request, *args, **kwargs):
        """
        Handles PUT and PATCH requests to update the menu item
        """
        partial_flag = kwargs.pop('partial', False)
        service = MenuItemService(view_object=self, request_object=request)
        data = service.update_menuitem(partial_flag=partial_flag)
        return success_response(
            message="Menu item Updated successfully", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
     
    @extend_schema(
        summary="Deletes menu item",
        description="Deletes individual menu item",
        responses={
            204: OpenApiResponse(description="No content"),
            404: OpenApiResponse(description="MenuItem not found")  
        },
        tags=['MenuItem']
    )
    def destroy(self, request, *args, **kwargs):    
        """
        Handles DELETE requests to delete a menuitem.
        Overridden to add custom Response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message="Menu item deleted successfully", 
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    
    @extend_schema(
        summary="Changes availability status of the menu item",
        description="Toggles availability status of the menu item",
        responses={
            200: MenuItemSerializer,
            404: OpenApiResponse(description="MenuItem not found")  
        },
        tags=['MenuItem'])  
    @action(
        detail=True, 
        methods=['post'], 
        url_path='toggle-availability',
        permission_classes=[IsAuthenticated, IsRestaurantOwner]
    )
    def toggle_availability(self, request, pk=None):
        """
        Handles PATCH requests to toggle availability status of perticular menu item.
        """
        service = MenuItemService(view_object=self, request_object=request)
        data = service.toggle_availability_status()
        
        return success_response(
            message="Menu item availability status changed successfully",
            data=data, 
            status_code=status.HTTP_200_OK
        )
        
    
    @extend_schema(
        summary="lists all reviews of menu item",
        description="retrieves list of reviews view related to menu item",
        responses={
            200: ReviewSerializer,
            404: OpenApiResponse(description="menu item not found")
        },
        tags=['Reviews']
    )
    @action(
        detail=True,
        methods=['get'],
        permission_classes = [AllowAny],
        serializer_class=ReviewSerializer,
        url_path="reviews"
    )
    def reviews(self, request, pk=None):
        """
        Retrieves all reviews related to perticular restaurants
        """
        menu_item_object = self.get_object()
        queryset = MenuItemSelector.get_reviews_of_menuitem(menu_item_object)
        serializer = ReviewSerializer(queryset, many=True)
        
        return success_response(
            message="Reviews of menu items",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )