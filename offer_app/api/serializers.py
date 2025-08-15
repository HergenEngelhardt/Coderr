from rest_framework import serializers
from offer_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for offer detail objects.
    
    Args:
        id: Detail ID
        title: Detail title
        revisions: Number of revisions
        delivery_time_in_days: Delivery time in days
        price: Detail price
        features: List of features
        offer_type: Type of offer (basic, standard, premium)
        
    Returns:
        OfferDetail: Serialized offer detail data
    """
    
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type'
        ]


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for offer detail URLs in offer lists.
    
    Args:
        id: Detail ID
        url: Detail URL
        
    Returns:
        dict: Detail ID and URL
    """
    
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
    
    def get_url(self, obj):
        """
        Generate URL for offer detail.
        
        Args:
            obj: OfferDetail instance
            
        Returns:
            str: URL path for the detail
        """
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/offerdetails/{obj.id}/')
        return f'/api/offerdetails/{obj.id}/'


class UserDetailsSerializer(serializers.Serializer):
    """
    Serializer for user details in offer lists.
    
    Args:
        first_name: User's first name
        last_name: User's last name
        username: User's username
        
    Returns:
        dict: User detail information
    """
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for offer list view with minimal details.
    
    Args:
        id: Offer ID
        user: User ID who created offer
        title: Offer title
        image: Offer image
        description: Offer description
        created_at: Creation timestamp
        updated_at: Update timestamp
        details: List of detail URLs
        min_price: Minimum price from details
        min_delivery_time: Minimum delivery time from details
        user_details: User information
        
    Returns:
        Offer: Serialized offer data for lists
    """
    
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'user', 
            'title', 
            'image', 
            'description', 
            'created_at', 
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
    
    def get_user_details(self, obj):
        """
        Get user details for offer.
        
        Args:
            obj: Offer instance
            
        Returns:
            dict: User detail information
        """
        user = obj.user
        return {
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'username': user.username
        }


class OfferDetailViewSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed offer view.
    
    Args:
        id: Offer ID
        user: User ID who created offer
        title: Offer title
        image: Offer image
        description: Offer description
        created_at: Creation timestamp
        updated_at: Update timestamp
        details: List of detail URLs
        min_price: Minimum price from details
        min_delivery_time: Minimum delivery time from details
        
    Returns:
        Offer: Serialized offer data with details
    """
    
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'user', 
            'title', 
            'image', 
            'description', 
            'created_at', 
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offers.
    
    Args:
        title: Offer title
        image: Offer image
        description: Offer description
        details: List of offer details
        
    Returns:
        Offer: Created or updated offer instance
        
    Raises:
        ValidationError: If offer doesn't have exactly 3 details
    """
    
    details = OfferDetailSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
    
    def validate_details(self, value):
        """
        Validate that offer has exactly 3 details for creation, allow partial updates.
        
        Args:
            value: List of detail data
            
        Returns:
            list: Validated detail data
            
        Raises:
            ValidationError: If not exactly 3 details for creation
        """
        # For creation (no instance exists), require exactly 3 details
        if not self.instance:
            if len(value) != 3:
                raise serializers.ValidationError(
                    "An offer must contain exactly 3 details."
                )
            
            offer_types = [detail['offer_type'] for detail in value]
            expected_types = ['basic', 'standard', 'premium']
            
            if set(offer_types) != set(expected_types):
                raise serializers.ValidationError(
                    "Offer must contain basic, standard, and premium details."
                )
        
        # For updates, validate that offer_types are valid if provided
        else:
            offer_types = [detail['offer_type'] for detail in value]
            valid_types = ['basic', 'standard', 'premium']
            
            for offer_type in offer_types:
                if offer_type not in valid_types:
                    raise serializers.ValidationError(
                        f"Invalid offer_type: {offer_type}. Must be one of: {valid_types}"
                    )
        
        return value
    
    def create(self, validated_data):
        """
        Create offer with details.
        
        Args:
            validated_data: Validated offer data
            
        Returns:
            Offer: Created offer instance
        """
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    
    def update(self, instance, validated_data):
        """
        Update offer and its details.
        
        Args:
            instance: Offer instance to update
            validated_data: Validated update data
            
        Returns:
            Offer: Updated offer instance
        """
        details_data = validated_data.pop('details', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                detail, created = OfferDetail.objects.get_or_create(
                    offer=instance,
                    offer_type=offer_type,
                    defaults=detail_data
                )
                if not created:
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
        
        return instance
