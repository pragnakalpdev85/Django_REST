from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from ..serializers import ReviewSerializer
from apps.restaurants.models import Review
from apps.restaurants.services import ReviewService
from apps.common.utils.permissions import IsCustomer
from apps.common.utils.custom_responses import success_response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.common.api.pagination import ReviewLimitOffsetPagination


@extend_schema_view(
    partial_update=extend_schema(
        summary="Updates Review data",
        description="Updates Review data partially or with whole data",
        responses={
            200: ReviewSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['Reviews']
    )
)
class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    
    list: Return a list of all existing reviews.
    create: Create a new review.
    retrieve: Return the review given by ID.
    update: Update all fields of review with a specific id.
    partial_update: Update only specified fields of a specific review.
    destroy: Delete a review instance.
    """
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = ReviewLimitOffsetPagination
    ordering = ['-created_at']


    def get_permission_classes(self):
        """
        Returns permission classes according to current action
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny]
        
        return [IsAuthenticated, IsCustomer]
        

    def get_queryset(self):
        """
        Returns queryset of the review model
        """
        
        return Review.objects.select_related(
            'customer', 'restaurant', 'menu_item', 'order', 'driver'
        )
        
        
    @extend_schema(
        summary="Retrieves lists of all reviews",
        description="Retrieves lists of all reviews data",
        responses={
            200: ReviewSerializer,
        },
        tags=['Reviews']
    )
    def list(self, request, *args, **kwargs):
        """
        Handles get request and list outs all reviews
        """
        service = ReviewService(view_object=self, request_object=request)
        data = service.list_review()
        
        return success_response(
            message="Reviews are retrieved successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )   
     
       
    @extend_schema(
        summary='Creates new review',
        description='Validates and creates new review',
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(description="Invalid data / Validation error") 
        },
        tags=['Reviews']
    )  
    def create(self, request, *args, **kwargs):
        """
        Handles post method of the review view
        """
        # request.data['customer'] = request.user.id
        service = ReviewService(view_object=self, request_object=request)
        data = service.create_review()
        
        return success_response(
            message="Review is created successfully",
            data=data,
            status_code=status.HTTP_201_CREATED
        )
    
       
    @extend_schema(
        summary="Retrieve review",
        description="Retrieve review with id",
        responses={
            200: Review,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['RestaurantProfile']
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Handles get request of review view
        """
        service = ReviewService(view_object=self, request_object=request)
        data = service.retrieve_review()
        
        return success_response(
            message="Review is retrieved successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
     
     
    @extend_schema(
        summary="Updates Review data",
        description="Updates Review data partially or with whole data",
        responses={
            200: ReviewSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['Reviews']
    )   
    def update(self, request, *args, **kwargs):
        """
        Handles Put and patch requsts
        """
        partial_flag = kwargs.pop("partial", False)
        service = ReviewService(view_object=self, request_object=request)
        data = service.update_review(partial_flag)
        
        return success_response(
            message="Review is updated successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
      
    @extend_schema(
        summary="Deletes Review",
        description="Deletes review by id",
        responses={
            204: OpenApiResponse(description="No Content"),
            404: OpenApiResponse(description="Profile not found")    
        },
        tags=['Reviews']
    )  
    def destroy(self, request, *args, **kwargs):
        """
        Handles delete method of the review
        """
        review = self.get_object()
        self.perform_destroy(review)

        return success_response(
            message="review deleted successfully", 
            data=None, 
            status_code=status.HTTP_204_NO_CONTENT
        )
        
        