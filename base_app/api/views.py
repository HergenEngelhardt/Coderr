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
        
    Raises:
        500: Internal server error
    """
    review_count = Review.objects.count()
    
    average_rating = Review.objects.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating']
    
    if average_rating is not None:
        average_rating = round(average_rating, 1)
    else:
        average_rating = 0.0
    
    business_profile_count = UserProfile.objects.filter(
        type='business'
    ).count()
    
    offer_count = Offer.objects.count()
    
    data = {
        'review_count': review_count,
        'average_rating': average_rating,
        'business_profile_count': business_profile_count,
        'offer_count': offer_count
    }
    
    serializer = BaseInfoSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)
