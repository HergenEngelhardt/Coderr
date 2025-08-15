from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from profile_app.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with profile creation.
    
    Args:
        username: Unique username string
        email: User email address
        password: User password
        repeated_password: Password confirmation
        type: User type (customer or business)
        
    Returns:
        dict: User data with token
        
    Raises:
        ValidationError: If passwords don't match or validation fails
    """
    
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES, 
        write_only=True
    )
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'repeated_password', 
            'type', 
            'token', 
            'user_id'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        """
        Validate password matching.
        
        Args:
            attrs: Attribute dictionary
            
        Returns:
            dict: Validated attributes
            
        Raises:
            ValidationError: If passwords don't match
        """
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        """
        Create user and profile with token.
        
        Args:
            validated_data: Validated user data
            
        Returns:
            User: Created user instance with token
        """
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        
        user = User.objects.create_user(**validated_data)
        
        UserProfile.objects.create(user=user, type=user_type)
        
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login authentication.
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        dict: User data with authentication token
        
    Raises:
        ValidationError: If credentials are invalid
    """
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    
    def validate(self, attrs):
        """
        Validate user credentials.
        
        Args:
            attrs: Attribute dictionary with username and password
            
        Returns:
            dict: Validated attributes with user data
            
        Raises:
            ValidationError: If credentials are invalid
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        
        refresh = RefreshToken.for_user(user)
        
        attrs['user'] = user
        attrs['token'] = str(refresh.access_token)
        attrs['email'] = user.email
        attrs['user_id'] = user.id
        
        return attrs
