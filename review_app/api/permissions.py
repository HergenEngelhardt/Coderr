from rest_framework.permissions import BasePermission


class IsCustomerUserForReview(BasePermission):
    """
    Permission class to allow only customer users to create reviews.
    
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


class IsReviewOwner(BasePermission):
    """
    Permission class to allow only review owners to edit their reviews.
    
    Args:
        request: HTTP request object
        view: View being accessed
        obj: Review object being accessed
        
    Returns:
        bool: True if user owns the review, False otherwise
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user owns the review.
        
        Args:
            request: HTTP request object
            view: View being accessed
            obj: Review object being accessed
            
        Returns:
            bool: True if user wrote this review
        """
        return obj.reviewer == request.user
