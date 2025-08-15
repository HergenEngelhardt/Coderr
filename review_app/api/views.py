from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from review_app.models import Review
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUserForReview, IsReviewOwner


class ReviewFilter(filters.FilterSet):
    """
    Filter class for review queryset filtering.
    
    Args:
        business_user_id: Filter by business user being reviewed
        reviewer_id: Filter by user who wrote the review
        ordering: Order by updated_at or rating
    """
    
    business_user_id = filters.NumberFilter(field_name='business_user__id')
    reviewer_id = filters.NumberFilter(field_name='reviewer__id')
    ordering = filters.OrderingFilter(fields=['updated_at', 'rating'])
    
    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List all reviews or create a new review.
    
    Args:
        request: HTTP request object
        
    Returns:
        Response: List of reviews or created review
        
    Raises:
        400: Invalid request data or user already reviewed
        401: User not authenticated
        403: User not customer type (for creation)
    """
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Get permissions for the view.
        
        Returns:
            list: List of permission instances
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUserForReview()]
        return [permissions.IsAuthenticated()]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a review.
    
    Args:
        request: HTTP request object
        pk: Primary key of review
        
    Returns:
        Response: Review data, updated review data, or empty response for delete
        
    Raises:
        400: Invalid request data
        401: User not authenticated
        403: User not owner of review
        404: Review not found
    """
    
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]
    
    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request method.
        
        Returns:
            Serializer: ReviewUpdateSerializer for PATCH/PUT, ReviewSerializer for GET
        """
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateSerializer
        return ReviewSerializer


class ReviewUpdateView(generics.UpdateAPIView):
    """
    Update a review (rating and description only).
    
    Args:
        request: HTTP request object
        pk: Primary key of review
        
    Returns:
        Response: Updated review data
        
    Raises:
        400: Invalid request data
        401: User not authenticated
        403: User not owner of review
        404: Review not found
    """
    
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]


class ReviewDeleteView(generics.DestroyAPIView):
    """
    Delete a review (owner only).
    
    Args:
        request: HTTP request object
        pk: Primary key of review
        
    Returns:
        Response: Empty response with 204 status
        
    Raises:
        401: User not authenticated
        403: User not owner of review
        404: Review not found
    """
    
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]
