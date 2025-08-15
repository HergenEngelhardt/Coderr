from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    order_count_view,
    completed_order_count_view
)


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', order_count_view, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count_view, name='completed-order-count'),
]
