from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from profile_app.models import UserProfile
from .serializers import (
    UserProfileSerializer, 
    BusinessProfileListSerializer,
    CustomerProfileListSerializer
)
from .permissions import IsOwnerOrReadOnly


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile details.
    
    Args:
        request: HTTP request object
        pk: Primary key of profile to retrieve/update
        
    Returns:
        Response: Profile data or error response
        
    Raises:
        401: User not authenticated
        403: User not owner of profile
        404: Profile not found
    """
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        """
        Get profile object by primary key.
        
        Returns:
            UserProfile: Profile instance
            
        Raises:
            404: Profile not found
        """
        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(UserProfile, user__id=pk)


class BusinessProfileListView(generics.ListAPIView):
    """
    List all business user profiles.
    
    Args:
        request: HTTP request object
        
    Returns:
        Response: List of business profiles
        
    Raises:
        401: User not authenticated
    """
    
    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get queryset of business profiles.
        
        Returns:
            QuerySet: Business user profiles
        """
        return UserProfile.objects.filter(type='business')


class CustomerProfileListView(generics.ListAPIView):
    """
    List all customer user profiles.
    
    Args:
        request: HTTP request object
        
    Returns:
        Response: List of customer profiles
        
    Raises:
        401: User not authenticated
    """
    
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get queryset of customer profiles.
        
        Returns:
            QuerySet: Customer user profiles
        """
        return UserProfile.objects.filter(type='customer')
