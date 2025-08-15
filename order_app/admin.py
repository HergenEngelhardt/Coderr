from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    
    Args:
        model: Order model class
        
    Returns:
        ModelAdmin: Configured admin interface
    """
    
    list_display = ['title', 'customer_user', 'business_user', 'status', 'price', 'created_at']
    list_filter = ['status', 'offer_type', 'created_at']
    search_fields = ['title', 'customer_user__username', 'business_user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer_user', 'business_user', 'title', 'status')
        }),
        ('Service Details', {
            'fields': ('offer_type', 'price', 'delivery_time_in_days', 'revisions')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
