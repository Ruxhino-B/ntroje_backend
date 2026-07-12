from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Agency, AgencyMember
from .permissions import IsAgencyMemberManagerOrReadOnly, IsAgencyOwnerOrReadOnly
from .serializers import (
    AgencyCreateUpdateSerializer,
    AgencyDetailSerializer,
    AgencyListSerializer,
    AgencyMemberCreateUpdateSerializer,
    AgencyMemberSerializer,
)


class AgencyListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/agency/agencies/
    POST /api/agency/agencies/
    """
    queryset = Agency.objects.select_related('owner').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AgencyCreateUpdateSerializer
        return AgencyListSerializer


class AgencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/agency/agencies/<id>/
    PUT    /api/agency/agencies/<id>/
    PATCH  /api/agency/agencies/<id>/
    DELETE /api/agency/agencies/<id>/
    """
    queryset = Agency.objects.select_related('owner').prefetch_related('members__user').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAgencyOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return AgencyCreateUpdateSerializer
        return AgencyDetailSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AgencyMemberListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/agency/agencies/<agency_id>/members/
    POST /api/agency/agencies/<agency_id>/members/
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AgencyMember.objects.select_related('agency', 'user').filter(
            agency_id=self.kwargs['agency_id']
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AgencyMemberCreateUpdateSerializer
        return AgencyMemberSerializer

    def perform_create(self, serializer):
        serializer.save(agency_id=self.kwargs['agency_id'])


class AgencyMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/agency/members/<id>/
    PUT    /api/agency/members/<id>/
    PATCH  /api/agency/members/<id>/
    DELETE /api/agency/members/<id>/
    """
    queryset = AgencyMember.objects.select_related('agency', 'user').all()
    permission_classes = [IsAuthenticated, IsAgencyMemberManagerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return AgencyMemberCreateUpdateSerializer
        return AgencyMemberSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)