from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse 

from apps.users.services import DriverService
from apps.common.utils.custom_responses import success_response
from apps.users.selectors import ProfileSelectors
from apps.restaurants.api.v1.serializers import ReviewSerializer
from apps.common.utils.permissions import IsRestaurantOwner, IsProfileOwner, IsOwnerOrReadOnly
from apps.users.api.v1.serializers import DriverProfileSerializer, DriverInfoSerializer


@extend_schema_view(
    partial_update=extend_schema(
        summary="Updates Driver Profile data",
        description="updates Driver profile data partially or with whole data",
        responses={
            200: DriverProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['DriverProfile']
    )
)
class DriverProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows driver profiles to be viewed or edited.
    
    list:Return a list of all existing drivers.
    create: Create a new driver profile.
    retrieve: Return the given driver by ID.
    update: Update all fields of a specific driver profile.
    partial_update: Update only specified fields of a specific driver profile.
    destroy: Delete a driver profile instance.
    """
    queryset = ProfileSelectors.get_driver_profile_queryset()
    
    def get_object(self):
        """
        checks permission at object level and returns object
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    def get_serializer_class(self):
        """
        Returns serilizer class based on action
        """
        if self.action == 'list':
            return DriverInfoSerializer
        
        return DriverProfileSerializer
    
    
    def get_permissions(self):
        """
        Returns permission classes as per authorized actions for users
        """
        if self.action == 'list':
            return [IsAuthenticated(), IsRestaurantOwner(), IsOwnerOrReadOnly()]
        
        return [IsAuthenticated(), IsProfileOwner(), IsOwnerOrReadOnly()]
        

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        pass
    
    @extend_schema(
        summary="Lists all drivers details",
        description="Lists all driver profile details with user informations",
        responses={
            200: DriverInfoSerializer,
        },
        tags=['Drivers']
    )
    def list(self, request, *args, **kwargs):
        """Lists outs all the drivers present"""
        service = DriverService(view_object=self, request_object=request)
        data = service.list_drivers()
        return success_response(
            "Drivers data retrieved", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieves driver profile data",
        description="Retrieves driver profile data",
        responses={
          200: DriverProfileSerializer,
          404: OpenApiResponse(description="Profile Not Found")  
        },
        tags=['DriverProfile']
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieves driver profile by id"""
        service = DriverService(view_object=self, request_object=request)
        data = service.retreive_driver_profile()
        return success_response(
            "Driver Profile retrieved", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Updates Driver Profile data",
        description="Updates Driver profile data partially or with whole data",
        responses={
            200: DriverProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['DriverProfile']
    )
    def update(self, request, *args, **kwargs):
        """Updates the driver profile by id (partially or full)"""
        partial_flag = kwargs.pop("partial", False)
        service = DriverService(view_object=self, request_object=request)
        data = service.update_driver_profile(partial_flag=partial_flag)
        return success_response(
            "Driver Profile Updated", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Deletes driver profile",
        description="Deletes driver profile",
        responses={
            204: OpenApiResponse(description="Profile deleted successfully"),
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['DriverProfile']
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes driver profile by id"""
        obj = self.get_object()
        obj.delete()
        return success_response(
            "Driver Profile is deleted", 
            status_code=status.HTTP_204_NO_CONTENT
        )
      
        
    @extend_schema(
        summary="Lists all active drivers details",
        description="Lists all active driver profile details with user informations",
        responses={
            200: DriverInfoSerializer,
        },
        tags=['Drivers'])
    @action(
        detail=False, 
        methods=['get'],
        serializer_class=DriverInfoSerializer,
        permission_classes=[IsAuthenticated, IsRestaurantOwner]
    )
    def active(self, request):
        """Lists all the active drivers """
        service = DriverService(view_object=self, request_object=request)
        data = service.list_active_drivers()
        
        return success_response(
            "Active drivers list retrieved",
            data=data, 
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Toggles availability of driver",
        description="Toggles availability status of the driver",
        responses={
            200: DriverProfileSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation Error")
        },
        tags=['DriverProfile'])
    @action(
        detail=True,    
        methods=['post'], 
        url_path='toggle-availability',
        permission_classes=[IsAuthenticated, IsProfileOwner]
    )
    def toggle_availability(self, request, pk=None):
        """Toggles driver's availability status"""
        service = DriverService(view_object=self, request_object=request)
        data = service.toggle_availability_status()
        
        return success_response(
            "Driver availability status updated", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
        
        
    @extend_schema(
        summary="lists all reviews of driver",
        description="retrieves list of reviews view related to driver",
        responses={
            200: ReviewSerializer,
            404: OpenApiResponse(description="Driver profile not found")
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
        queryset = ProfileSelectors.get_reviews_of_driver(driver=profile_object)
        serializer = ReviewSerializer(queryset, many=True)
        
        return success_response(
            message="Reviews of Restaurant",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
    @extend_schema(
        summary="Uploads Driver avatar",
        description="Upload image of the Driver profile avatar",
        responses={
            200: DriverProfileSerializer,
            404: OpenApiResponse(description="Profile not found")
        },
        tags=['DriverProfile'])
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsProfileOwner],
        serializer_class=DriverProfileSerializer,
        url_path="upload-avatar"
    )
    def upload_avatar(self, request, pk=None, *args, **kwargs):
        """
        Uploads image to an driver's profile
        """
        profile_object = self.get_object()
        data = {'avatar': request.data.get('avatar', None)}
        serializer = self.get_serializer(instance=profile_object, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            "Avatar Uploaded successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
