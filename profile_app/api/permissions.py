from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners to edit their profiles.
    
    Args:
        request: HTTP request object
        view: View being accessed
        obj: Object being accessed
        
    Returns:
        bool: True if permission granted, False otherwise
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access object.
        
        Args:
            request: HTTP request object
            view: View being accessed
            obj: Object being accessed
            
        Returns:
            bool: True if user owns the profile or read-only access
        """
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.user == request.user
