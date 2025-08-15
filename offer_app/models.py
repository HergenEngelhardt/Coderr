from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """
    Model representing a freelancer's service offer.
    
    Args:
        user: Foreign key to User model (business user)
        title: Offer title string
        image: Optional offer image
        description: Detailed offer description
        created_at: Auto-generated creation timestamp
        updated_at: Auto-updated modification timestamp
        
    Returns:
        Offer: An offer instance
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ['-updated_at']
    
    def __str__(self):
        """
        String representation of Offer.
        
        Returns:
            str: Title and user combination
        """
        return f"{self.title} by {self.user.username}"
    
    @property
    def min_price(self):
        """
        Calculate minimum price from offer details.
        
        Returns:
            float: Minimum price from all details
        """
        details = self.details.all()
        if details:
            return min(detail.price for detail in details)
        return 0
    
    @property
    def min_delivery_time(self):
        """
        Calculate minimum delivery time from offer details.
        
        Returns:
            int: Minimum delivery time in days
        """
        details = self.details.all()
        if details:
            return min(detail.delivery_time_in_days for detail in details)
        return 0


class OfferDetail(models.Model):
    """
    Model representing specific details/packages of an offer.
    
    Args:
        offer: Foreign key to Offer model
        title: Detail package title
        revisions: Number of revisions included
        delivery_time_in_days: Delivery time in days
        price: Package price
        features: List of features as JSON
        offer_type: Type of package (basic, standard, premium)
        
    Returns:
        OfferDetail: An offer detail instance
    """
    
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    offer = models.ForeignKey(
        Offer, 
        on_delete=models.CASCADE, 
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=10, 
        choices=OFFER_TYPE_CHOICES
    )
    
    class Meta:
        verbose_name = "Offer Detail"
        verbose_name_plural = "Offer Details"
        unique_together = ['offer', 'offer_type']
    
    def __str__(self):
        """
        String representation of OfferDetail.
        
        Returns:
            str: Title and offer type combination
        """
        return f"{self.title} ({self.offer_type})"
