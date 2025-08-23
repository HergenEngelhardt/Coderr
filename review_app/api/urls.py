from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    BusinessUserReviewStatsView
)


urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('business-users/<int:business_user_id>/review-stats/', 
         BusinessUserReviewStatsView.as_view(), 
         name='business-user-review-stats'),
]
