from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ['business_user', 'reviewer']
        ordering = ['-updated_at']
    
    def __str__(self):
        """
        String representation of Review.
        
        Returns:
            str: Reviewer and business user combination with rating
        """
        return f"{self.reviewer.username} -> {self.business_user.username} ({self.rating}/5)"
