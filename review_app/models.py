from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError


class Review(models.Model):
    """
    Model representing a review from customer to business user.
    
    Args:
        business_user: Foreign key to User model (business being reviewed)
        reviewer: Foreign key to User model (customer writing review)
        rating: Rating from 1 to 5
        description: Review description text
        created_at: Auto-generated creation timestamp
        updated_at: Auto-updated modification timestamp
        
    Returns:
        Review: A review instance
    """
    
    business_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="received_reviews"
    )
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="written_reviews"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (worst) to 5 (best)"
    )
    description = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text="Review description (minimum 10 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ['business_user', 'reviewer']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['business_user', '-created_at']),
            models.Index(fields=['reviewer', '-created_at']),
            models.Index(fields=['rating']),
        ]
    
    def clean(self):
        """
        Custom validation to prevent self-reviews.
        """
        if self.business_user == self.reviewer:
            raise ValidationError("Users cannot review themselves.")
    
    def save(self, *args, **kwargs):
        """
        Override save to call clean validation.
        """
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        """
        String representation of Review.
        
        Returns:
            str: Reviewer and business user combination with rating
        """
        return f"{self.reviewer.username} -> {self.business_user.username} ({self.rating}/5)"
    
    @property
    def is_positive(self):
        """
        Check if review is positive (rating >= 4).
        
        Returns:
            bool: True if rating is 4 or 5
        """
        return self.rating >= 4
    
    @property
    def is_negative(self):
        """
        Check if review is negative (rating <= 2).
        
        Returns:
            bool: True if rating is 1 or 2
        """
        return self.rating <= 2
    
    @classmethod
    def get_average_rating(cls, business_user):
        """
        Calculate average rating for a business user.
        
        Args:
            business_user: User instance to calculate average for
            
        Returns:
            float: Average rating or 0 if no reviews
        """
        reviews = cls.objects.filter(business_user=business_user)
        if not reviews.exists():
            return 0
        return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
