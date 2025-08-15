from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with custom field handling.
    
    Args:
        user: User ID
        username: Username from related user
        first_name: First name from related user
        last_name: Last name from related user
        file: Profile picture file
        location: User location
        tel: Telephone number
        description: User description
        working_hours: Working hours for business users
        type: User type (customer/business)
        email: Email from related user
        created_at: Profile creation timestamp
        
    Returns:
        UserProfile: Serialized profile data
    """
    
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    user = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type', 
            'email',
            'created_at'
        ]
    
    def to_representation(self, instance):
        """
        Custom representation to ensure empty strings instead of null.
        
        Args:
            instance: UserProfile instance
            
        Returns:
            dict: Serialized data with empty strings for null fields
        """
        data = super().to_representation(instance)
        
        fields_to_convert = [
            'first_name', 
            'last_name', 
            'location', 
            'tel', 
            'description', 
            'working_hours'
        ]
        
        for field in fields_to_convert:
            if data.get(field) is None:
                data[field] = ''
        
        return data
    
    def update(self, instance, validated_data):
        """
        Update profile and related user data.
        
        Args:
            instance: UserProfile instance to update
            validated_data: Validated data for update
            
        Returns:
            UserProfile: Updated profile instance
        """
        user_data = validated_data.pop('user', {})
        
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for business profile lists.
    
    Args:
        user: User ID
        username: Username from related user
        first_name: First name from related user
        last_name: Last name from related user
        file: Profile picture file
        location: User location
        tel: Telephone number
        description: User description
        working_hours: Working hours
        type: User type
        
    Returns:
        UserProfile: Serialized business profile data
    """
    
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type'
        ]
    
    def to_representation(self, instance):
        """
        Custom representation to ensure empty strings instead of null.
        
        Args:
            instance: UserProfile instance
            
        Returns:
            dict: Serialized data with empty strings for null fields
        """
        data = super().to_representation(instance)
        
        fields_to_convert = [
            'first_name', 
            'last_name', 
            'location', 
            'tel', 
            'description', 
            'working_hours'
        ]
        
        for field in fields_to_convert:
            if data.get(field) is None:
                data[field] = ''
        
        return data


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for customer profile lists.
    
    Args:
        user: User ID
        username: Username from related user
        first_name: First name from related user
        last_name: Last name from related user
        file: Profile picture file
        uploaded_at: Upload timestamp for file
        type: User type
        
    Returns:
        UserProfile: Serialized customer profile data
    """
    
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at',
            'type'
        ]
