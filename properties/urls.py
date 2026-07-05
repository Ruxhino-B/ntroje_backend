from django.urls import path

from .views import (
    PropertyDetailView,
    PropertyImageDeleteView,
    PropertyImageUploadView,
    PropertyListCreateView,
)

urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),

    path('<int:property_id>/images/', PropertyImageUploadView.as_view(), name='property-image-upload'),
    path('images/<int:pk>/', PropertyImageDeleteView.as_view(), name='property-image-delete'),
]