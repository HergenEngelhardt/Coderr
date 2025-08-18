from rest_framework import serializers
from offer_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for offer detail objects.
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
    """
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for offer list view with minimal details.
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
        return self.create_user_dict(user)
    
    def create_user_dict(self, user):
        """
        Create user dictionary.
        
        Args:
            user: User instance
            
        Returns:
            dict: User information
        """
        return {
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'username': user.username
        }


class OfferDetailViewSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed offer view.
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
    """
    
    details = OfferDetailSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
    
    def validate_details(self, value):
        """
        Validate that offer has exactly 3 details for creation.
        
        Args:
            value: List of detail data
            
        Returns:
            list: Validated detail data
            
        Raises:
            ValidationError: If not exactly 3 details for creation
        """
        if not self.instance:
            self.validate_creation_details(value)
        else:
            self.validate_update_details(value)
        
        return value
    
    def validate_creation_details(self, value):
        """
        Validate details for offer creation.
        
        Args:
            value: List of detail data
            
        Raises:
            ValidationError: If not exactly 3 details
        """
        if len(value) != 3:
            raise serializers.ValidationError("An offer must contain exactly 3 details.")
        
        self.validate_offer_types(value)
    
    def validate_update_details(self, value):
        """
        Validate details for offer update.
        
        Args:
            value: List of detail data
            
        Raises:
            ValidationError: If invalid offer types
        """
        self.validate_offer_types_update(value)
    
    def validate_offer_types(self, value):
        """
        Validate offer types for creation.
        
        Args:
            value: List of detail data
            
        Raises:
            ValidationError: If missing required types
        """
        offer_types = [detail['offer_type'] for detail in value]
        expected_types = ['basic', 'standard', 'premium']
        
        if set(offer_types) != set(expected_types):
            raise serializers.ValidationError(
                "Offer must contain basic, standard, and premium details."
            )
    
    def validate_offer_types_update(self, value):
        """
        Validate offer types for update.
        
        Args:
            value: List of detail data
            
        Raises:
            ValidationError: If invalid offer types
        """
        offer_types = [detail['offer_type'] for detail in value]
        valid_types = ['basic', 'standard', 'premium']
        
        for offer_type in offer_types:
            if offer_type not in valid_types:
                raise serializers.ValidationError(
                    f"Invalid offer_type: {offer_type}. Must be one of: {valid_types}"
                )
    
    def create(self, validated_data):
        """
        Create offer with details.
        
        Args:
            validated_data: Validated offer data
            
        Returns:
            Offer: Created offer instance
        """
        details_data = validated_data.pop('details')
        offer = self.create_offer(validated_data)
        self.create_offer_details(offer, details_data)
        
        return offer
    
    def create_offer(self, validated_data):
        """
        Create offer object.
        
        Args:
            validated_data: Validated offer data
            
        Returns:
            Offer: Created offer instance
        """
        return Offer.objects.create(**validated_data)
    
    def create_offer_details(self, offer, details_data):
        """
        Create offer details.
        
        Args:
            offer: Offer instance
            details_data: List of detail data
        """
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
    
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
        
        self.update_offer_fields(instance, validated_data)
        
        if details_data:
            self.update_offer_details(instance, details_data)
        
        return instance
    
    def update_offer_fields(self, instance, validated_data):
        """
        Update offer fields.
        
        Args:
            instance: Offer instance
            validated_data: Validated data
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
    
    def update_offer_details(self, instance, details_data):
        """
        Update offer details.
        
        Args:
            instance: Offer instance
            details_data: List of detail data
        """
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            detail, created = OfferDetail.objects.get_or_create(
                offer=instance,
                offer_type=offer_type,
                defaults=detail_data
            )
            if not created:
                self.update_detail_fields(detail, detail_data)
    
    def update_detail_fields(self, detail, detail_data):
        """
        Update detail fields.
        
        Args:
            detail: OfferDetail instance
            detail_data: Detail data
        """
        for attr, value in detail_data.items():
            setattr(detail, attr, value)
        detail.save()