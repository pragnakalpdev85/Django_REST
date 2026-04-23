from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view

from apps.users.services import CustomerService
from apps.users.selectors import ProfileSelectors
from apps.common.utils.custom_responses import success_response
from apps.users.api.v1.serializers import CustomerProfileSerializer
from apps.common.api.pagination import CustomerProfilePageNumberPagination
from apps.common.utils.permissions import IsProfileOwner, IsOwnerOrReadOnly
from apps.users.models import CustomerProfile

@extend_schema_view(
    partial_update=extend_schema(
        summary="Updates Customer Profile data",
        description="updates Customer profile data partially or with whole data",
        responses={
            200: CustomerProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['CustomerProfile']
    )
)
class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customer profiles to be viewed or edited.
    
    list: Return a list of all existing Customer.
    create: Create a new customer profile.
    retrieve: Return the given customer by ID.
    update: Update all fields of a specific customer profile.
    partial_update: Update only specified fields of a specific customer profile.
    destroy: Delete a customer profile instance.
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner, IsOwnerOrReadOnly]
    queryset = ProfileSelectors.get_customer_profile_queryset()
    pagination_class = CustomerProfilePageNumberPagination
    
    def get_object(self):
        """
        checks permission at object level and returns object
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    @extend_schema(exclude = True)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    @extend_schema(
        summary="Lists all cutomer Profiles",
        description="Lists all customers data",
        responses={
            200:CustomerProfileSerializer
        },
        tags=['CustomerProfile']
    )
    def list(self, request, *args, **kwargs):
        """Lists all customers"""
        obj = self.get_queryset()
        serializer = self.get_serializer(obj, many=True)
        
        return success_response(
            message="List of Customers",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieves Customer Profile data",
        description="Retrieves Customer profile data from data base",
        responses={
            200: CustomerProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile']
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieves customer profile by id"""
        
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        
        return success_response(
            "Customer Profile Retrieved", 
            data=serializer.data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Updates Customer Profile data",
        description="updates Customer profile data partially or with whole data",
        responses={
            200: CustomerProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['CustomerProfile']
    )
    def update(self, request, *args, **kwargs):
        """Updates customer profile partialy of fully"""
        
        partial_flag = kwargs.pop('partial', False)
        service = CustomerService(view_object=self, request_object=request)
        data = service.update_profile(partial_flag)
        
        return success_response(
            "Customer Profile Updated", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Deletes Customer Profile data",
        description="Deletes Customer profile data from data base",
        responses={
            204: OpenApiResponse(description="Profile deleted successfully"),
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile']
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes customer profile by id"""
        
        obj = self.get_object()
        obj.delete()
        
        return success_response(
            "Customer Profile deleted", 
            status_code=status.HTTP_204_NO_CONTENT
        )    