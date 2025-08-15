from rest_framework import serializers


class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for platform base information.
    
    Args:
        review_count: Total number of reviews
        average_rating: Average rating across all reviews
        business_profile_count: Number of business profiles
        offer_count: Total number of offers
        
    Returns:
        dict: Platform statistics data
    """
    
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
