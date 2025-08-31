from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from order_app.models import Order
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    OrderCountSerializer,
    CompletedOrderCountSerializer
)
from .permissions import (
    IsCustomerUser,
    IsBusinessUserForOrder,
    IsOrderParticipant
)


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List orders for authenticated user or create new order.
    
    Args:
        request: HTTP request object
        
    Returns:
        Response: List of user's orders or created order
        
    Raises:
        400: Invalid request data
        401: User not authenticated
        403: User not customer type (for creation)
        404: Offer detail not found
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        
        Returns:
            Serializer: Appropriate serializer for the action
        """
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create order and return it with OrderSerializer for proper response format.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Use OrderSerializer for response to exclude offer_detail_id
        response_serializer = OrderSerializer(order)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_permissions(self):
        """
        Get permissions for the view.
        
        Returns:
            list: List of permission instances
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """
        Get orders for current user.
        
        Returns:
            QuerySet: Orders where user is customer or business user
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an order.
    
    Args:
        request: HTTP request object
        pk: Primary key of order
        
    Returns:
        Response: Order data, updated order data, or empty response for delete
        
    Raises:
        400: Invalid request data
        401: User not authenticated
        403: User not authorized for this order
        404: Order not found
    """
    
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOrderParticipant]
    
    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request method.
        
        Returns:
            Serializer: OrderStatusUpdateSerializer for PATCH/PUT, OrderSerializer for GET
        """
        if self.request.method in ['PATCH', 'PUT']:
            return OrderStatusUpdateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        """
        Get permissions for the view.
        
        Returns:
            list: List of permission instances
        """
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.request.method in ['PATCH', 'PUT']:
            return [permissions.IsAuthenticated(), IsBusinessUserForOrder()]
        return [permissions.IsAuthenticated(), IsOrderParticipant()]


class OrderUpdateView(generics.UpdateAPIView):
    """
    Update order status (business users only).
    
    Args:
        request: HTTP request object
        pk: Primary key of order
        
    Returns:
        Response: Updated order data
        
    Raises:
        401: User not authenticated
        403: User not business user for this order
        404: Order not found
    """
    
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessUserForOrder]


class OrderDeleteView(generics.DestroyAPIView):
    """
    Delete order (admin/staff only).
    
    Args:
        request: HTTP request object
        pk: Primary key of order
        
    Returns:
        Response: Empty response with 204 status
        
    Raises:
        401: User not authenticated
        403: User not staff
        404: Order not found
    """
    
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_count_view(request, business_user_id):
    """
    Get count of in-progress orders for business user.
    
    Args:
        request: HTTP request object
        business_user_id: ID of business user
        
    Returns:
        Response: Order count data
        
    Raises:
        401: User not authenticated
        404: Business user not found
    """
    business_user = get_object_or_404(User, id=business_user_id)
    
    order_count = Order.objects.filter(
        business_user=business_user,
        status='in_progress'
    ).count()
    
    serializer = OrderCountSerializer({'order_count': order_count})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def completed_order_count_view(request, business_user_id):
    """
    Get count of completed orders for business user.
    
    Args:
        request: HTTP request object
        business_user_id: ID of business user
        
    Returns:
        Response: Completed order count data
        
    Raises:
        401: User not authenticated
        404: Business user not found
    """
    business_user = get_object_or_404(User, id=business_user_id)
    
    completed_count = Order.objects.filter(
        business_user=business_user,
        status='completed'
    ).count()
    
    serializer = CompletedOrderCountSerializer({
        'completed_order_count': completed_count
    })
    return Response(serializer.data, status=status.HTTP_200_OK)
