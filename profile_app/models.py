from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extended user profile model for both customer and business users.
    
    Args:
        user: OneToOne relationship with Django's User model
        file: Profile picture image field
        location: User's location string
        tel: Telephone number string
        description: User description text
        working_hours: Business working hours string
        type: User type (customer or business)
        
    Returns:
        UserProfile: A user profile instance
    """
    
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='customer'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        """
        String representation of UserProfile.
        
        Returns:
            str: Username and type combination
        """
        return f"{self.user.username} ({self.type})"
