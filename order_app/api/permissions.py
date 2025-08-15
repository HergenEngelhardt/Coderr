from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Permission class to allow only customer users to create orders.
    
    Args:
        request: HTTP request object
        view: View being accessed
        
    Returns:
        bool: True if user is customer type, False otherwise
    """
    
    def has_permission(self, request, view):
        """
        Check if user has customer profile type.
        
        Args:
            request: HTTP request object
            view: View being accessed
            
        Returns:
            bool: True if user is authenticated and has customer profile
        """
        if not request.user.is_authenticated:
            return False
        
        try:
            return request.user.profile.type == 'customer'
        except AttributeError:
            return False


class IsBusinessUserForOrder(BasePermission):
    """
    Permission class to allow only business users to update order status.
    
    Args:
        request: HTTP request object
        view: View being accessed
        obj: Order object being accessed
        
    Returns:
        bool: True if user is business type, False otherwise
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is business user for the order.
        
        Args:
            request: HTTP request object
            view: View being accessed
            obj: Order object being accessed
            
        Returns:
            bool: True if user is business user for this order
        """
        try:
            return (request.user.profile.type == 'business' and 
                   obj.business_user == request.user)
        except AttributeError:
            return False


class IsOrderParticipant(BasePermission):
    """
    Permission class to allow only order participants to view orders.
    
    Args:
        request: HTTP request object
        view: View being accessed
        obj: Order object being accessed
        
    Returns:
        bool: True if user is participant in order, False otherwise
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is customer or business user for the order.
        
        Args:
            request: HTTP request object
            view: View being accessed
            obj: Order object being accessed
            
        Returns:
            bool: True if user is part of this order
        """
        return (obj.customer_user == request.user or 
                obj.business_user == request.user)
