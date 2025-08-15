from django.urls import path
from .views import base_info_view


urlpatterns = [
    path('base-info/', base_info_view, name='base-info'),
]
