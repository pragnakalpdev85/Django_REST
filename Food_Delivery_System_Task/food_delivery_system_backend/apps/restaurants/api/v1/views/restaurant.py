from django.db.models import Count
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.common.api.filters import RestaurantFilters
from apps.restaurants.services import RestaurantService
from apps.restaurants.models import RestaurantProfile, Review
from apps.restaurants.selectors import RestaurantSelector
from apps.common.utils.custom_responses import success_response
from apps.restaurants.api.v1.serializers import ReviewSerializer
from apps.common.api.pagination import RestaurantPageNumberPagination
from apps.common.utils.permissions import IsRestaurantOwner, IsProfileOwner, IsOwnerOrReadOnly
from ..serializers import (
    RestaurantProfileSerializer, 
    RestaurantMenuItemSerializer, 
    RestaurantInfoSerializer,
    RestaurantCreateUpdateSerializer
)
from apps.common.utils.constants import (
    RESTAURANT_CACHE_TIMEOUT,
    RESTAURANT_PROFILE_CACHE_TIMEOUT,
    POPULAR_RESTAURANT_CACHE_TIMEOUT,
    MENUITEM_CACHE_TIMEOUT
)

  
@extend_schema_view(
    partial_update=extend_schema(
        summary="Updates Restaurant Profile data",
        description="Updates Restaurant profile data partially or with whole data",
        responses={
            200: RestaurantProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['RestaurantProfile']
    )
)
class RestaurantProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Restaurant profiles to be viewed or edited.
    
    list: Return a list of all existing Restaurant.
    create: Create a new Restaurant profile.
    retrieve: Return the restaurant profile given by ID.
    update: Update all fields of a specific Restaurant profile.
    partial_update: Update only specified fields of a specific Restaurant profile.
    destroy: Delete a Restaurant profile instance.
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilters
    pagination_class = RestaurantPageNumberPagination
    
    
    def get_queryset(self):
        """
        Returns the queryset for Restaurant profiles
        """
        
        return RestaurantSelector.get_restaurant_profile_queryset()
          
        
    def get_serializer_class(self):
        """
        Returns serializer classes based on the current action
        """
        
        if self.action == 'list':
            return RestaurantInfoSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RestaurantCreateUpdateSerializer
        
        return RestaurantProfileSerializer
        
        
    def get_permissions(self):
        """
        Returns permission classes based on the current action
        """
        
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsRestaurantOwner()]
        
        return [IsAuthenticated(), IsProfileOwner(), IsRestaurantOwner(), IsOwnerOrReadOnly()]
    
    def get_object(self):
        """
        checks permission at object level and returns object
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    
    @extend_schema(
        summary='Creates new restaurant profile',
        description='Validates and creates new profile of restaurant',
        responses={
            201: RestaurantProfileSerializer,
            400: OpenApiResponse(description="Invalid data / Validation error") 
        },
        tags=['RestaurantProfile']
    )
    def create(self, request, *args, **kwargs):
        """
        Creates new restaurants profile
        """
        service = RestaurantService(view_object=self, request_object=request)
        data = service.create_restaurant_profile()
        return success_response(
            message = "New Profile is created successfully",
            data=data,
            status_code=status.HTTP_201_CREATED
        )
    
    
    @extend_schema(
        summary="Retrieves lists of all restaurants",
        description="Retrieves lists of all restaurants data with name, description and other essential informations",
        responses={
            200: RestaurantInfoSerializer,
        },
        tags=['Restaurants']
    )
    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to list restaurant profiles.
        """
        cache_key = f"restaurant_list_{request.META.get('QUERY_STRING', '')}"
        cached = cache.get(cache_key)
        if cached is not None:
            return success_response(
                message="List of restaurant retrieved successfully",
                data=cached, 
                status_code=status.HTTP_200_OK
            )
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_data, RESTAURANT_CACHE_TIMEOUT)
            return success_response(
                message="List of restaurant retrieved successfully",
                data=paginated_data, 
                status_code=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(queryset, many=True)
        
        cache.set(cache_key, serializer.data, RESTAURANT_CACHE_TIMEOUT)
        return success_response(
            message="List of restaurant retrieved successfully",
            data=serializer.data, 
            status_code=status.HTTP_200_OK
        )
        
        
    @extend_schema(
        summary="Retrieve restaurant profile",
        description="Retrieve restaurant profile of owner",
        responses={
            200: RestaurantProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['RestaurantProfile']
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET request to retrieve restaurant profile
        """
        cache_key = f"restaurant_detail_{kwargs.get('pk')}"
        cached = cache.get(cache_key)
        if cached is not None:
            return success_response(
                message="Restaurant profile retrieved successfully",
                data=cached,
                status_code=status.HTTP_200_OK
            )
        
        service = RestaurantService(view_object=self, request_object=request)
        data = service.retrieve_restaurant_profile()
        
        cache.set(cache_key, data, RESTAURANT_PROFILE_CACHE_TIMEOUT)
        
        return success_response(
            message="Restaurant profile retrieved successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Updates restaurant profile",
        description="Updates retaurant profile partially or with whole data",
        responses={
            200: RestaurantProfileSerializer,
            400: OpenApiResponse(description="Invalid input / Validation error")
        },
        tags=['RestaurantProfile']
    )
    def update(self, request, *args, **kwargs):
        """
        Handles PUT or Patch requests to update restaurant profile
        """
        partial_flag = kwargs.pop("partial", False)
        service = RestaurantService(view_object=self, request_object=request)
        data = service.update_restaurant_profile(partial_flag=partial_flag)
        return success_response(
            message="Restaurant profile updated successfully", 
            data=data, 
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Deletes Restaurant profile",
        description="Deletes restaurant profile",
        responses={
            204: OpenApiResponse(description="No Content"),
            404: OpenApiResponse(description="Profile not found")    
        },
        tags=['RestaurantProfile']
    )
    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE requests to delete a restaurant.
        Overridden to add custom Response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return success_response(
            message="Restaurant profile deleted successfully", 
            data=None, 
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    
    @extend_schema(
        summary="Retrieves list of active restaurants",
        description="Retrieves all restaurants which are open now",
        responses={
            200:RestaurantInfoSerializer,
        },
        tags=['Restaurants'])
    @action(
        detail=False, 
        methods=['get'],
        permission_classes=[AllowAny],
        serializer_class=RestaurantInfoSerializer,
    )
    def active(self, request):
        """
        Handles GET requests to list all active restaurants.
        """
        queryset = RestaurantSelector.get_active_restaurants()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            message="Active restaurants are retrieved",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieve list of menu items of specific restaurant",
        description="Retrieve list of menu items of specific restaurant",
        responses={
            200: RestaurantMenuItemSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['RestaurantProfile'])
    @action(
        detail=True, 
        methods=['get'],
        permission_classes=[AllowAny], 
    )
    def menu(self, request, pk=None):
        """
        Handles GET requests to list all menu items of perticular restaurant.
        """
        cache_key = f"restaurant_menu_{pk}"
        cached = cache.get(cache_key)
        if cached is not None:
            return success_response(
                message="Menu item of restaurant retrieved successfully",
                data=cached, 
                status_code=status.HTTP_200_OK
            )
        
        items = self.get_queryset().filter(pk=pk).first()
        serializer = RestaurantMenuItemSerializer(items.restaurant_menuitem, many = True)
        
        cache.set(cache_key, serializer.data, MENUITEM_CACHE_TIMEOUT)
        items = {'restaurant_menuitem': serializer.data}
        return success_response(
            message="Menu item of restaurant retrieved successfully",
            data=items, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieves list of popular restaurants",
        description="Retrieves top 10 restaurants with highest rating",
        responses={
            200:RestaurantInfoSerializer,
        },
        tags=['Restaurants'])
    @action(
        detail=False, 
        methods=['get'],
        permission_classes=[AllowAny],
        serializer_class=RestaurantInfoSerializer,  
    )
    def popular(self, request):
        """
        Handles GET requests to list top 10 popular restaurants.
        """
        cache_key = f"restaurant_popular"
        cached = cache.get(cache_key)
        if cached is not None:
            return success_response(
                message="10 Most popular restaurants",
                data=cached, 
                status_code=status.HTTP_200_OK
            )
        
        queryset = RestaurantSelector.get_popular_restaurants()
        serializer = self.get_serializer(queryset, many = True)
        cache.set(cache_key, serializer.data, POPULAR_RESTAURANT_CACHE_TIMEOUT)
        
        return success_response(
            message="10 Most popular restaurants",
            data=serializer.data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieve all restaurant profile of current user",
        description="Retrieve all restaurant profile of current user",
        responses={
            200: RestaurantInfoSerializer,    
        },
        tags=['Restaurants'])
    @action(
        detail=False,
        methods=['get'],
        permission_classes = [IsAuthenticated, IsRestaurantOwner],
        serializer_class = RestaurantInfoSerializer,
        url_path="owner-restaurants"
    )
    def owner_restaurants(self, request):
        """
        Handles Get request to list all restaurant profile of current owner
        """
        queryset = RestaurantSelector.get_restaurant_profile_by_user(restaurant_owner=request.user)
        serializer = self.get_serializer(queryset, many = True)
        
        return success_response(
            message="All restaurant profile of current owner is retrieved",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
    
    @extend_schema(
        summary="lists all reviews of restaurant",
        description="retrieves list of reviews view related to restaurant",
        responses={
            200: ReviewSerializer,
            404: OpenApiResponse(description="Restaurant profile not found")
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
        profile_object = self.get_object()
        queryset = RestaurantSelector.get_restaurant_reviews(profile_object)
        serializer = ReviewSerializer(queryset, many=True)
        
        return success_response(
            message="Reviews of Restaurant",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
    
    @extend_schema(
        summary="Uploads Restaurant logo",
        description="Upload image of the restaurant profile logo",
        responses={
            200: RestaurantProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['RestaurantProfile'])
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=RestaurantProfileSerializer,
        url_path="upload-logo"
    )
    def upload_logo(self, request, pk=None, *args, **kwargs):
        """
        Uploads image to an restaurant's profile
        """
        profile_object = self.get_object()
        data = {'logo': request.data.get('logo', None)}
        serializer = self.get_serializer(instance=profile_object, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            "logo Uploaded successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
    @extend_schema(
        summary="Uploads Restaurant banner",
        description="Upload image of the restaurant profile banner",
        responses={
            200: RestaurantProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['RestaurantProfile'])
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=RestaurantProfileSerializer,
        url_path="upload-banner"
    )
    def upload_banner(self, request, pk=None, *args, **kwargs):
        """
        Uploads image to an restaurant's profile
        """
        profile_object = self.get_object()
        data = {'banner': request.data.get('banner', None)}
        serializer = self.get_serializer(instance=profile_object, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            "banner Uploaded successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )