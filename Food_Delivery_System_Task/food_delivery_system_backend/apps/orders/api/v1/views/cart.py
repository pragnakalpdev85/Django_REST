from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.orders.models import OrderItem
from apps.orders.selectors import OrderCartSelector
from apps.restaurants.models import MenuItem
from apps.orders.services import CartService
from apps.orders.api.v1.serializers import CartSerializer, OrderMenuItemSerializer, OrderItemCreateSerializer
from apps.common.utils.permissions import IsCustomer
from apps.common.utils.custom_responses import success_response


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customer carts.
    Provides complete CRUD operations restricted to the authenticated customer.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [UserRateThrottle]


    def get_queryset(self):
        """
        Return the cart for the currently authenticated customer.
        Prefetches cart_menu to optimize database queries.
        """
        user = self.request.user
        if hasattr(user, 'customer'):
            return OrderCartSelector.get_cart_by_customer(user.customer)
        return OrderCartSelector.get_empty_cart()


    @extend_schema(
        summary="List customer's cart",
        description="Retrieve the cart details of the authenticated customer.",
        responses={200: CartSerializer(many=True)},
        tags=['Cart'],
    )
    def list(self, request, *args, **kwargs):
        """
        Lists cart
        """
        response = super().list(request, *args, **kwargs)
        return success_response(
            message="Cart retrieved successfully",
            data=response.data,
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Create a cart",
        description="Create a new cart for the authenticated customer.",
        request=CartSerializer,
        responses={201: CartSerializer},
        tags=['Cart'],
    )
    def create(self, request, *args, **kwargs):
        """
        Creates cart
        """
        response = super().create(request, *args, **kwargs)
        return success_response(
            message="Cart created successfully",
            data=response.data,
            status_code=status.HTTP_201_CREATED
        )


    @extend_schema(
        summary="Retrieve cart details",
        description="Retrieve specific details of a cart by ID.",
        responses={200: CartSerializer},
        tags=['Cart'],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves cart by id
        """
        response = super().retrieve(request, *args, **kwargs)
        return success_response(
            message="Cart retrieved successfully",
            data=response.data,
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Update a cart",
        description="Update the entire cart for the authenticated customer.",
        request=CartSerializer,
        responses={200: CartSerializer},
        tags=['Cart'],
    )
    def update(self, request, *args, **kwargs):
        """
        Updates whole cart
        """
        
        response = super().update(request, *args, **kwargs)
        return success_response(
            message="Cart updated successfully",
            data=response.data,
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Partially update a cart",
        description="Update specific fields of a cart for the authenticated customer.",
        request=CartSerializer,
        responses={200: CartSerializer},
        tags=['Cart'],
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Updates partially
        """
        response = super().partial_update(request, *args, **kwargs)
        return success_response(
            message="Cart updated successfully",
            data=response.data,
            status_code=status.HTTP_200_OK
        )


    @extend_schema(
        summary="Delete a cart",
        description="Delete the cart of the authenticated customer.",
        responses={204: OpenApiResponse(description="Cart deleted successfully.")},
        tags=['Cart'],
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return success_response(
            message="Cart deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    
    @extend_schema(
        summary="Add orderitem to cart",
        description="Adds new order item to the customer's cart",
        responses={
            200: OpenApiResponse(description="Orderitem added"),
            400: OpenApiResponse(description="Invalid input / Validation error")
        },
        tags=['Cart'])   
    @action(
        detail=False,
        methods=['post'],
        url_path='add-to-cart',
        permission_classes=[IsAuthenticated, IsCustomer],
        serializer_class=OrderItemCreateSerializer,
    )
    def add_to_cart(self, request):
        """
        Adds order item to the cart
        """
        service = CartService(view_object=self, request_object=request)
        data = service.add_order_item_to_cart()
    
        return success_response(
            message="OrderItem added successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )
        
    
    @extend_schema(
        summary="Remove orderitem from cart",
        description="Removes orderitem from customer's cart",
        responses={
            200: OpenApiResponse(description="Orderitem removed"),
            400: OpenApiResponse(description="Invalid input / Validation error")
        },
        tags=['Cart'])
    @action(
        detail=False,
        methods=['post'],
        url_path='remove-from-cart',
        permission_classes=[IsAuthenticated, IsCustomer],
        serializer_class=OrderMenuItemSerializer,
    )
    def remove_from_cart(self, request):
        """
        Removes order item from the cart
        """
        service = CartService(view_object=self, request_object=request)
        data = service.remove_order_item_from_cart()
        
        return success_response(
            message="Order item removed from cart successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )

    
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in customer's profile to the new cart.
        """
        serializer.save(customer=self.request.user.customer)