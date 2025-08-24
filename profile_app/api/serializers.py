from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles.
    Converts UserProfile objects to JSON and back.
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
        Converts null values to empty strings.
        This prevents null values from being sent to frontend.
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
        Updates profile and related user data.
        Saves both UserProfile and User changes.
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
    Simple serializer for business profile lists.
    Shows only important information for business customers.
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
        Converts null values to empty strings.
        Prevents null values in API response.
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
    Simple serializer for customer profile lists.
    Shows only important information for private customers.
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
            'location',
            'tel',
            'description',
            'working_hours',
            'uploaded_at',
            'type'
        ]
    
    def to_representation(self, instance):
        """
        Converts null values to empty strings.
        Prevents null values in API response.
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