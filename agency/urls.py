from django.urls import path

from .views import (
    AgencyDetailView,
    AgencyListCreateView,
    AgencyMemberDetailView,
    AgencyMemberListCreateView,
)

app_name = 'agency'

urlpatterns = [
    path('agencies/', AgencyListCreateView.as_view(), name='agency-list-create'),
    path('agencies/<int:pk>/', AgencyDetailView.as_view(), name='agency-detail'),
    path('agencies/<int:agency_id>/members/', AgencyMemberListCreateView.as_view(), name='agency-member-list-create'),
    path('members/<int:pk>/', AgencyMemberDetailView.as_view(), name='agency-member-detail'),
]