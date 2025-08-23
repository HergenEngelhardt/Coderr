from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from review_app.models import Review
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUserForReview, IsReviewOwner


class ReviewFilter(filters.FilterSet):
    """
    Filter class for review queryset filtering.
    
    Args:
        business_user_id: Filter by business user being reviewed
        reviewer_id: Filter by user who wrote the review
        rating: Filter by exact rating or rating range
        rating_min: Filter by minimum rating
        rating_max: Filter by maximum rating
        ordering: Order by updated_at, created_at or rating
    """
    
    business_user_id = filters.NumberFilter(field_name='business_user__id')
    reviewer_id = filters.NumberFilter(field_name='reviewer__id')
    rating = filters.NumberFilter(field_name='rating')
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    ordering = filters.OrderingFilter(fields=['updated_at', 'created_at', 'rating'])
    
    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id', 'rating']


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
    
    queryset = Review.objects.select_related('business_user', 'reviewer').all()
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
    
    def perform_create(self, serializer):
        """
        Save the review with the current user as reviewer.
        
        Args:
            serializer: Review serializer instance
        """
        serializer.save(reviewer=self.request.user)


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
    
    queryset = Review.objects.select_related('business_user', 'reviewer').all()
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


class BusinessUserReviewStatsView(generics.GenericAPIView):
    """
    Get review statistics for a business user.
    
    Args:
        request: HTTP request object
        business_user_id: ID of business user
        
    Returns:
        Response: Review statistics (average rating, total count, rating distribution)
        
    Raises:
        404: Business user not found
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, business_user_id):
        """
        Get review statistics for a specific business user.
        
        Args:
            request: HTTP request object
            business_user_id: ID of the business user
            
        Returns:
            Response: Statistics data
        """
        try:
            from django.contrib.auth.models import User
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Business user not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        reviews = Review.objects.filter(business_user=business_user)
        
        # Basic statistics
        stats = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        # Rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[f'rating_{i}'] = reviews.filter(rating=i).count()
        
        # Positive/Negative review counts
        positive_reviews = reviews.filter(rating__gte=4).count()
        negative_reviews = reviews.filter(rating__lte=2).count()
        neutral_reviews = reviews.filter(rating=3).count()
        
        response_data = {
            'business_user_id': business_user_id,
            'business_user_name': business_user.username,
            'average_rating': round(stats['average_rating'] or 0, 2),
            'total_reviews': stats['total_reviews'],
            'positive_reviews': positive_reviews,
            'neutral_reviews': neutral_reviews,
            'negative_reviews': negative_reviews,
            'rating_distribution': rating_distribution
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
