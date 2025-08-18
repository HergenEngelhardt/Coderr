from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Permission class to allow only business users to create offers.
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
        
        return self.check_user_profile(request.user)
    
    def check_user_profile(self, user):
        """
        Check if user has business profile.
        
        Args:
            user: User object
            
        Returns:
            bool: True if user has business profile
        """
        try:
            return user.profile.type == 'business'
        except AttributeError:
            return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class to allow only owners to edit their offers.
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
        if self.is_read_only_request(request):
            return True
        
        return self.is_owner(obj, request.user)
    
    def is_read_only_request(self, request):
        """
        Check if request is read-only.
        
        Args:
            request: HTTP request object
            
        Returns:
            bool: True if request is read-only
        """
        return request.method in ['GET', 'HEAD', 'OPTIONS']
    
    def is_owner(self, obj, user):
        """
        Check if user owns the object.
        
        Args:
            obj: Object being accessed
            user: User making request
            
        Returns:
            bool: True if user owns the object
        """
        return obj.user == user