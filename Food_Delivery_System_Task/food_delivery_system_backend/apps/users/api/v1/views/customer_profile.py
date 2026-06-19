from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework.decorators import action

from apps.users.services import CustomerService
from apps.users.selectors import ProfileSelectors
from apps.common.utils.custom_responses import success_response
from apps.users.api.v1.serializers import CustomerProfileSerializer, CustomerAddressSerializer, AddressSerializer
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
        
    @extend_schema(
        summary="Uploads customers avatar",
        description="Upload image of the customer profile avatar",
        responses={
            200: CustomerProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile'])
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=CustomerProfileSerializer,
        url_path="upload-avatar"
    )
    def upload_avatar(self, request, pk=None, *args, **kwargs):
        """
        Uploads image to an customer's profile
        """
        profile_object = self.get_object()
        data = {'avatar': request.data.get('avatar', None)}
        serializer = self.get_serializer(
            instance=profile_object,
            data=data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Return the full profile using your original serializer
        return success_response(
            "Avatar Uploaded successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Retrieves list of customer's saved addresses",
        description="Retrieves list of customer's saved addresses from saved address json field",
        responses={
            200: CustomerAddressSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile'])
    @action(
        detail=True, 
        methods=['get'],
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=CustomerAddressSerializer,
        url_path="list-addresses"
    )
    def list_addresses(self, request):
        """Get all addresses."""
        customer_profile = self.get_object()
        serializer = self.get_serializer(customer_profile)
        return success_response(
            message="List of saved addresses retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Creates a new customer's saved addresses",
        description="Creates a new customer's saved addresses for saved address json field",
        responses={
            200: CustomerAddressSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile'])
    @action(
        detail=True, 
        methods=['post'],
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=CustomerAddressSerializer,
        url_path="create-address"
    )
    def create_address(self, request):
        """Add a new address to the JSON list."""
        customer_profile = self.get_object()
        serializer = AddressSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        address_data = serializer.validated_data
        address_data['id'] = str(uuid.uuid4()) # Generate unique ID for management
        
        # Initialize list if null
        if not customer_profile.saved_address: 
            customer_profile.saved_address = []
            
        customer_profile.saved_address.append(address_data)
        customer_profile.save()
        serializer = self.get_serializer(customer_profile.saved_address)
        return success_response(
            message="Address created successfully.",
            data=serializer.data, 
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Updates a customer's saved addresses",
        description="Updates a customer's saved addresses for saved address json field",
        responses={
            200: CustomerAddressSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile'])
    @action(
        detail=True, 
        methods=['put', 'patch'], 
        permission_classes=[IsAuthenticated, IsProfileOwner],
        serializer_class=CustomerAddressSerializer,
        url_path='update-address/(?P<address_id>[^/.]+)'
    )
    def update_address(self, request, address_id=None):
        """Update an existing address by its ID."""
        customer_profile = self.get_object()
        addresses = customer_profile.saved_address or []
        
        # Find target address
        address_index = next((index for (index, d) in enumerate(addresses) if d.get('id') == address_id), None)
        
        if address_index is None:
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = AddressSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Merge old data with updated fields
        updated_data = {**addresses[address_index], **serializer.validated_data}
        addresses[address_index] = updated_data
        
        customer_profile.saved_address = addresses
        customer_profile.save()
        serializer = self.get_serializer(customer_profile.saved_address)
        return success_response(
            message="Address updated successfully",
            data=serializer.data, 
            status_code=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Deletes a customer's saved addresses",
        description="Delete a customer's saved addresses from saved address json field",
        responses={
            204: OpenApiResponse(description="No Content"),
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['CustomerProfile'])
    @action(
        detail=True, 
        methods=['delete'], 
        permission_classes=[IsAuthenticated, IsProfileOwner],
        url_path='delete-address/(?P<address_id>[^/.]+)'
    )
    def delete_address(self, request, address_id=None):
        """Remove an address by its ID."""
        customer_profile = self.get_object()
        addresses = customer_profile.saved_address or []
        
        new_addresses = [addr for addr in addresses if addr.get('id') != address_id]
        
        if len(addresses) == len(new_addresses):
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
            
        customer_profile.saved_address = new_addresses
        customer_profile.save()
        return success_response(
            message="Address deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

        