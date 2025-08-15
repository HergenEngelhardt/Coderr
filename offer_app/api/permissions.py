from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Permission class to allow only business users to create offers.
    
    Args:
        request: HTTP request object
        view: View being accessed
        
    Returns:
        bool: True if user is business type, False otherwise
    """
    
    def has_permission(self, request, view):
        """
        Check if user has business profile type.
        
        Args:
            request: HTTP request object
            view: View being accessed
            
        Returns:
            bool: True if user is authenticated and has business profile
        """
        if not request.user.is_authenticated:
            return False
        
        try:
            return request.user.profile.type == 'business'
        except AttributeError:
            return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class to allow only owners to edit their offers.
    
    Args:
        request: HTTP request object
        view: View being accessed
        obj: Object being accessed
        
    Returns:
        bool: True if permission granted, False otherwise
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user owns the offer.
        
        Args:
            request: HTTP request object
            view: View being accessed
            obj: Offer object being accessed
            
        Returns:
            bool: True if user owns the offer or read-only access
        """
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.user == request.user
