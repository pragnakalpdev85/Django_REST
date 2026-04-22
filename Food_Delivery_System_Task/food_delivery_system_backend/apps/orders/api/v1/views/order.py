from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.orders.services import OrderService
from apps.common.utils.permissions import IsCustomer, IsRestaurantOwner
from apps.common.api.filters import OrderFilters
from apps.orders.selectors import OrderCartSelector
from apps.common.api.pagination import OrdersCursorPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..serializers import OrderSerializer, OrderCreateSerializer
from apps.common.utils.custom_responses import success_response


@extend_schema_view(
    partial_update = extend_schema(
        summary="Updates order",
        description="Updates order partially or whole menu item",
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description="Order not found")  
        },
        tags=['Orders']
    )  
)
class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    
    list: Return a list of all existing order
    create: Create a new order.
    retrieve: Return the order given by ID.
    update: Update all fields of order with a specific id.
    partial_update: Update only specified fields of a specific order.
    destroy: Delete a order instance.
    """
    serializer_class = OrderSerializer
    ordering = ['-created_at']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilters
    pagination_class = OrdersCursorPagination
    
    def get_permission_classes(self):
        """
        Returns permission classes based on current actions
        """
        if self.action == 'list':
            return [IsAuthenticated, IsRestaurantOwner]
        
        return [IsAuthenticated, IsCustomer] or [IsAuthenticated, IsRestaurantOwner]
        
    
    def get_serializer_class(self):
        """
        Returns serializer class based on current actions
        """
        if self.action == 'create':
            return OrderCreateSerializer
        
        return OrderSerializer

    def get_queryset(self):
        """Reassigning queryset"""
        base = OrderCartSelector.get_order_queryset()
        return base
    
    
    @extend_schema(
        summary="List of all orders",
        description="Retrieve list of all orders",
        responses={
            200: OrderSerializer  
        },
        tags=['Orders']
    )
    def list(self, request, *args, **kwargs):
        """
        handles GET request and lists all orders
        """
        service = OrderService(view_object=self, request_object=request)
        order = service.list_orders()
        
        return success_response(
            message="Orders are retrieved successfully",
            data=order,
            status_code=status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Retrieves order",
        description="Retrieves individual order",
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description="Order not found")  
        },
        tags=['Orders']
    )  
    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve data of a menu item 
        with id.
        """
        service = OrderService(view_object=self, request_object=request)
        data = service.retrieve_order()
        return success_response(
            message = "Order retrieved successfully",
            data = data,
            status_code = status.HTTP_200_OK
        )
    
    
    @extend_schema(
        summary="Creates new order",
        description="Creates new order with order items",
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Invalid input / Validation error")
        },
        tags=['Orders']
    )
    def create(self, request, *args, **kwargs):
        """
        Handles POST request and Creates a new order with order items
        """
        service = OrderService(view_object=self, request_object=request)
        order = service.create_order()
        
        return success_response(
            message="Order is created successfully",
            data=order,
            status_code=status.HTTP_201_CREATED
        )
        
    @extend_schema(
        summary="Updates order",
        description="Updates individual order partially or whole menu item",
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description="order not found")  
        },
        tags=['Orders']
    )  
    def update(self, request, *args, **kwargs):
        """
        Handles PUT or PATCH requests and Updates order
        """
        partial_flag = kwargs.pop('partial', False)
        service = OrderService(view_object=self, request_object=request)
        data = service.update_order(partial_flag=partial_flag)
        return success_response(
            message="Order Updated successfully", 
            data=data, 
            status_code=status.HTTP_200_OK
        )
        
        
    @extend_schema(
        summary="Deletes order",
        description="Deletes individual order",
        responses={
            204: OpenApiResponse(description="No content"),
            404: OpenApiResponse(description="order not found")  
        },
        tags=['Orders']
    )
    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE request and deletes a perticular order
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return success_response(
            message="Order deleted successfully", 
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
        

    @extend_schema(
        summary="Assign driver to an order",
        description="Assigns driver to an order",
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Invalid Input / Validation error")
        },
        tags=['Orders'])
    @action(
        detail=True, 
        methods=['post'], 
        url_path='assign-driver',
        serializer_class=OrderSerializer,
        permission_classes=[AllowAny]
    )
    def assign_driver(self, request, pk=None):
        "Assign_driver to the perticular order"
        service = OrderService(view_object=self, request_object=request)
        data = service.assign_driver_to_order()
        
        return success_response(
            message="Driver assigned to order successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
        
        
    @extend_schema(
        summary="Cancels order",
        description="Checks order can be cancel or not if can than cancel order",
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Cannot cancel order / Invalid Input / Validation Error")
        },
        tags=['Orders'])
    @action(
        detail=True, 
        methods=['post'], 
        url_path='cancel',
        serializer_class=OrderSerializer,
        permission_classes=[AllowAny]
    )
    def cancel(self, request, pk=None):
        """Cancel order with specific order id"""
        service = OrderService(view_object=self, request_object=request)
        data = service.cancel_order()
        
        return success_response(
            message="Order cancelled successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Changes status of an order",
        description="Updates status of an order",
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Cannot change status / Invalid Input / Validation Error")
        },
        tags=['Orders'])
    @action(
        detail=True, 
        methods=['post'], 
        url_path='update-status',
        permission_classes=[AllowAny],
        serializer_class=OrderSerializer    
    )
    def update_status(self, request, pk=None):
        """Update status of the perticular order"""
        service = OrderService(view_object=self, request_object=request)
        data = service.update_order_status()
        
        return success_response(
            message="Order status updated successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
    

    @extend_schema(
        summary="Lists active orders",
        description="Retrieves all active orders",
        responses={
            200: OrderSerializer
        },
        tags=['Orders'])
    @action(
        detail=False, 
        methods=['get'], 
        url_path='active',
        permission_classes=[AllowAny],
        serializer_class=OrderSerializer
    )
    def active(self, request):
        """Lists all active orders"""
        service = OrderService(view_object=self, request_object=request)
        data = service.list_active_orders()
        
        return success_response(
            message="Active orders retrieved successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
        
    
    @extend_schema(
        summary="Retrieves orders history",
        description="Retrieves all orders which are delivered or cancelled",
        responses={
            200: OrderSerializer
        },
        tags=['Orders'])
    @action(
        detail=False, 
        methods=['get'], 
        url_path='history',
        permission_classes=[IsAuthenticated],
        serializer_class=OrderSerializer 
    )  
    def history(self, request):
        """List all canceled or delivered data"""
        service = OrderService(view_object=self, request_object=request)
        data = service.list_history_of_orders()
        
        return success_response(
            message="Orders history retrieved successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
    
    
