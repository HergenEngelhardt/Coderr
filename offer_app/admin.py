from django.contrib import admin
from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """
    Inline admin for OfferDetail within Offer admin.
    
    Args:
        model: OfferDetail model class
        
    Returns:
        TabularInline: Configured inline interface
    """
    
    model = OfferDetail
    extra = 0
    fields = ['title', 'offer_type', 'price', 'delivery_time_in_days', 'revisions']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin configuration for Offer model.
    
    Args:
        model: Offer model class
        
    Returns:
        ModelAdmin: Configured admin interface
    """
    
    list_display = ['title', 'user', 'min_price', 'min_delivery_time', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'min_price', 'min_delivery_time']
    inlines = [OfferDetailInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'image', 'description')
        }),
        ('Calculated Fields', {
            'fields': ('min_price', 'min_delivery_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """
    Admin configuration for OfferDetail model.
    
    Args:
        model: OfferDetail model class
        
    Returns:
        ModelAdmin: Configured admin interface
    """
    
    list_display = ['title', 'offer', 'offer_type', 'price', 'delivery_time_in_days']
    list_filter = ['offer_type', 'offer__created_at']
    search_fields = ['title', 'offer__title', 'offer__user__username']
