from django.db.models import Avg
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from review_app.models import Review
from profile_app.models import UserProfile
from offer_app.models import Offer
from .serializers import BaseInfoSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def base_info_view(request):
    """
    Get general platform statistics.
    
    Args:
        request: HTTP request object
        
    Returns:
        Response: Platform base information
    """
    review_count = get_review_count()
    average_rating = get_average_rating()
    business_count = get_business_profile_count()
    offer_count = get_offer_count()
    
    data = create_stats_data(review_count, average_rating, business_count, offer_count)
    
    serializer = BaseInfoSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_review_count():
    """
    Get total number of reviews.
    
    Returns:
        int: Total review count
    """
    return Review.objects.count()


def get_average_rating():
    """
    Calculate average rating from all reviews.
    
    Returns:
        float: Average rating rounded to 1 decimal place
    """
    average = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    if average is not None:
        return round(average, 1)
    else:
        return 0.0


def get_business_profile_count():
    """
    Get number of business profiles.
    
    Returns:
        int: Business profile count
    """
    return UserProfile.objects.filter(type='business').count()


def get_offer_count():
    """
    Get total number of offers.
    
    Returns:
        int: Total offer count
    """
    return Offer.objects.count()


def create_stats_data(review_count, average_rating, business_count, offer_count):
    """
    Create dictionary with platform statistics.
    
    Args:
        review_count (int): Number of reviews
        average_rating (float): Average rating
        business_count (int): Number of business profiles
        offer_count (int): Number of offers
        
    Returns:
        dict: Platform statistics data
    """
    return {
        'review_count': review_count,
        'average_rating': average_rating,
        'business_profile_count': business_count,
        'offer_count': offer_count
    }