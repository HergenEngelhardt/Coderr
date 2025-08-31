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
    View for displaying and editing user profiles.
    Only the profile owner can edit their profile.
    """
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        """
        Gets the profile based on user ID.
        Returns 404 if profile does not exist.
        """
        pk = self.kwargs.get('pk')
        obj = generics.get_object_or_404(UserProfile, user__id=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class BusinessProfileListView(generics.ListAPIView):
    """
    View for displaying all business profiles.
    Shows a list of all business customers.
    """
    
    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Disable pagination as per specifications
    
    def get_queryset(self):
        """
        Filters only business profiles from database.
        Returns all profiles with type='business'.
        """
        return UserProfile.objects.filter(type='business')


class CustomerProfileListView(generics.ListAPIView):
    """
    View for displaying all customer profiles.
    Shows a list of all private customers.
    """
    
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Disable pagination as per specifications
    
    def get_queryset(self):
        """
        Filters only customer profiles from database.
        Returns all profiles with type='customer'.
        """
        return UserProfile.objects.filter(type='customer')