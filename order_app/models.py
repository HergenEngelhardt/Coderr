from django.contrib.auth.models import User
from django.db import models
from offer_app.models import OfferDetail


class Order(models.Model):
    """
    Model representing an order placed by a customer.
    
    Args:
        customer_user: Foreign key to User model (customer)
        business_user: Foreign key to User model (business)
        title: Order title from offer detail
        revisions: Number of revisions included
        delivery_time_in_days: Delivery time in days
        price: Order price
        features: List of features as JSON
        offer_type: Type of offer (basic, standard, premium)
        status: Current order status
        created_at: Auto-generated creation timestamp
        updated_at: Auto-updated modification timestamp
        
    Returns:
        Order: An order instance
    """
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    customer_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="customer_orders"
    )
    business_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="business_orders"
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
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='in_progress'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        """
        String representation of Order.
        
        Returns:
            str: Title and customer combination
        """
        return f"{self.title} - {self.customer_user.username}"
