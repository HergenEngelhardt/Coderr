from django_filters import rest_framework as filters
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from offer_app.models import Offer, OfferDetail
from .serializers import (
    OfferListSerializer,
    OfferDetailViewSerializer, 
    OfferCreateUpdateSerializer,
    OfferDetailSerializer
)
from .permissions import IsBusinessUser, IsOwnerOrReadOnly


class OfferPagination(PageNumberPagination):
    """Custom pagination for offers endpoint."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferFilter(filters.FilterSet):
    """
    Filter class for offer queryset filtering.
    """
    
    creator_id = filters.NumberFilter(field_name='user__id')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')
    ordering = filters.OrderingFilter(fields=['updated_at', 'min_price'])
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time', 'search']
    
    def filter_min_price(self, queryset, name, value):
        """
        Filter offers by minimum price.
        
        Args:
            queryset: Offer queryset
            name: Field name
            value: Minimum price value
            
        Returns:
            QuerySet: Filtered queryset
        """
        return queryset.filter(details__price__gte=value).distinct()
    
    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filter offers by maximum delivery time.
        
        Args:
            queryset: Offer queryset  
            name: Field name
            value: Maximum delivery time value
            
        Returns:
            QuerySet: Filtered queryset
        """
        return queryset.filter(details__delivery_time_in_days__lte=value).distinct()
    
    def filter_search(self, queryset, name, value):
        """
        Search offers by title and description.
        
        Args:
            queryset: Offer queryset
            name: Field name
            value: Search term
            
        Returns:
            QuerySet: Filtered queryset
        """
        return queryset.filter(
            models.Q(title__icontains=value) | 
            models.Q(description__icontains=value)
        )


class OfferListCreateView(generics.ListCreateAPIView):
    """
    List all offers or create a new offer.
    """
    
    queryset = Offer.objects.all()
    filterset_class = OfferFilter
    pagination_class = OfferPagination
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        
        Returns:
            Serializer: Appropriate serializer for the action
        """
        if self.request.method == 'POST':
            return OfferCreateUpdateSerializer
        return OfferListSerializer
    
    def get_permissions(self):
        """
        Get permissions for the view.
        
        Returns:
            list: List of permission instances
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return []
    
    def perform_create(self, serializer):
        """
        Perform offer creation with current user.
        
        Args:
            serializer: Validated serializer instance
        """
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offer.
    """
    
    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        
        Returns:
            Serializer: Appropriate serializer for the action
        """
        if self.is_update_request():
            return OfferCreateUpdateSerializer
        return OfferDetailViewSerializer
    
    def update(self, request, *args, **kwargs):
        """
        Update offer and return it with full details including IDs.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        
        response_serializer = OfferCreateUpdateSerializer(updated_instance)
        return Response(response_serializer.data)
    
    def is_update_request(self):
        """
        Check if request is update request.
        
        Returns:
            bool: True if request is PUT or PATCH
        """
        return self.request.method in ['PUT', 'PATCH']


class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    Retrieve specific offer detail by ID.
    """
    
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]