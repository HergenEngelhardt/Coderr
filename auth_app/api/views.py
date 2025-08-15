from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    """
    Handle user registration.
    
    Args:
        request: HTTP request with registration data
        
    Returns:
        Response: Success response with user data and token
        
    Raises:
        400: Invalid request data
        500: Internal server error
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'token': user.token,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handle user login authentication.
    
    Args:
        request: HTTP request with login credentials
        
    Returns:
        Response: Success response with user data and token
        
    Raises:
        400: Invalid credentials or request data
        500: Internal server error
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response({
            'token': serializer.validated_data['token'],
            'username': serializer.validated_data['username'],
            'email': serializer.validated_data['email'],
            'user_id': serializer.validated_data['user_id']
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
