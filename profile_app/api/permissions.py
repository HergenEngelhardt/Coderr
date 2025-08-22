from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission for profile owners.
    Only allows profile owner to edit their profile.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Checks if user is authorized.
        Read access for everyone, write access only for owner.
        """
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.user == request.user