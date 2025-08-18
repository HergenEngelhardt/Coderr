from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from profile_app.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
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
        Check if passwords match.
        
        Args:
            attrs (dict): Form data from user
            
        Returns:
            dict: The same data if valid
            
        Raises:
            ValidationError: When passwords don't match
        """
        password = attrs.get('password')
        repeated_password = attrs.get('repeated_password')
        
        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return attrs
    
    def create(self, validated_data):
        """
        Make new user account.
        
        Args:
            validated_data (dict): Clean user data
            
        Returns:
            User: New user with token
        """
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        
        user = self._create_user(validated_data)
        self._create_user_profile(user, user_type)
        user.token = self._generate_token(user)
        
        return user
    
    def _create_user(self, user_data):
        """
        Create user in database.
        
        Args:
            user_data (dict): Username, email, password
            
        Returns:
            User: Created user object
        """
        return User.objects.create_user(**user_data)
    
    def _create_user_profile(self, user, user_type):
        """
        Create profile for user.
        
        Args:
            user (User): User object
            user_type (str): Type of user account
            
        Returns:
            UserProfile: Created profile object
        """
        return UserProfile.objects.create(user=user, type=user_type)
    
    def _generate_token(self, user):
        """
        Make access token for user.
        
        Args:
            user (User): User object
            
        Returns:
            str: Access token string
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    
    def validate(self, attrs):
        """
        Check if login is correct.
        
        Args:
            attrs (dict): Username and password
            
        Returns:
            dict: User data with token
            
        Raises:
            ValidationError: When login fails
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = self._check_user_credentials(username, password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        
        return self._prepare_login_response(attrs, user)
    
    def _check_user_credentials(self, username, password):
        """
        Verify username and password.
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            User or None: User if valid, None if invalid
        """
        return authenticate(username=username, password=password)
    
    def _prepare_login_response(self, attrs, user):
        """
        Prepare data to send back after login.
        
        Args:
            attrs (dict): Original form data
            user (User): Authenticated user
            
        Returns:
            dict: Complete response data
        """
        refresh = RefreshToken.for_user(user)
        
        attrs['user'] = user
        attrs['token'] = str(refresh.access_token)
        attrs['email'] = user.email
        attrs['user_id']