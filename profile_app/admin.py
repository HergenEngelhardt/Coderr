from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    
    Args:
        model: UserProfile model class
        
    Returns:
        ModelAdmin: Configured admin interface
    """
    
    list_display = ['user', 'type', 'location', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'type')
        }),
        ('Profile Details', {
            'fields': ('file', 'location', 'tel', 'description', 'working_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
