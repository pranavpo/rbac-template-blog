from django.urls import path
from .views import BlogViewSet

urlpatterns = [
    path('blogs/', BlogViewSet.as_view({'get': 'list', 'post': 'create'}), name='blog-list'),
    path('blogs/<int:pk>/', BlogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='blog-detail'),
    path('blogs/<int:pk>/update-status/', BlogViewSet.as_view({'patch': 'update_status'}), name='blog-update-status'),
]
