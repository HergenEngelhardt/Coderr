from rest_framework import serializers
from django.contrib.auth.models import User
from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for review objects.
    
    Args:
        id: Review ID
        business_user: Business user being reviewed (ID)
        reviewer: User writing the review (ID)
        rating: Rating from 1 to 5
        description: Review description text
        created_at: Creation timestamp
        updated_at: Update timestamp
        
    Returns:
        Review: Serialized review data
    """
    
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']
    
    def validate_business_user(self, value):
        """
        Validate that business user exists and is business type.
        
        Args:
            value: Business user ID
            
        Returns:
            User: Validated business user
            
        Raises:
            ValidationError: If user not found or not business type
        """
        try:
            user = User.objects.get(id=value.id)
            if user.profile.type != 'business':
                raise serializers.ValidationError(
                    "Can only review business users."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError("Business user not found.")
        except AttributeError:
            raise serializers.ValidationError("User has no profile.")
        
        return value
    
    def validate(self, attrs):
        """
        Validate that reviewer can review this business user.
        
        Args:
            attrs: Attribute dictionary
            
        Returns:
            dict: Validated attributes
            
        Raises:
            ValidationError: If reviewer already reviewed this business user
        """
        request = self.context.get('request')
        business_user = attrs.get('business_user')
        
        if request and business_user:
            existing_review = Review.objects.filter(
                business_user=business_user,
                reviewer=request.user
            ).first()
            
            if existing_review and not self.instance:
                raise serializers.ValidationError(
                    "You have already reviewed this business user."
                )
        
        return attrs
    
    def create(self, validated_data):
        """
        Create review with current user as reviewer.
        
        Args:
            validated_data: Validated review data
            
        Returns:
            Review: Created review instance
        """
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating reviews (rating and description only).
    
    Args:
        rating: Updated rating from 1 to 5
        description: Updated review description
        
    Returns:
        Review: Updated review instance
    """
    
    class Meta:
        model = Review
        fields = ['rating', 'description']
