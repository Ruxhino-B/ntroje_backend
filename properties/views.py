from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Property, PropertyImage
from .permissions import IsPropertyOwnerOrReadOnly
from .serializers import (
    PropertyCreateUpdateSerializer,
    PropertyDetailSerializer,
    PropertyImageSerializer,
    PropertyImageUploadSerializer,
    PropertyListSerializer,
)


class PropertyListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/properties/
    POST /api/properties/
    """
    queryset = Property.objects.select_related('owner').prefetch_related('images').filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'address', 'city', 'country']
    ordering_fields = ['price', 'area', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyCreateUpdateSerializer
        return PropertyListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/properties/<id>/
    PUT    /api/properties/<id>/
    PATCH  /api/properties/<id>/
    DELETE /api/properties/<id>/
    """
    queryset = Property.objects.select_related('owner').prefetch_related('images').filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly, IsPropertyOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PropertyCreateUpdateSerializer
        return PropertyDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)


class PropertyImageUploadView(generics.GenericAPIView):
    """
    POST /api/properties/<property_id>/images/
    Upload maximum 20 images per property.
    """
    serializer_class = PropertyImageUploadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPropertyOwnerOrReadOnly]

    def get_property(self):
        property_obj = generics.get_object_or_404(
            Property.objects.prefetch_related('images'),
            pk=self.kwargs['property_id'],
            is_active=True
        )
        self.check_object_permissions(self.request, property_obj)
        return property_obj

    def post(self, request, *args, **kwargs):
        property_obj = self.get_property()

        serializer = self.get_serializer(
            data=request.data,
            context={'property': property_obj}
        )
        serializer.is_valid(raise_exception=True)

        created_images = []
        for index, image in enumerate(serializer.validated_data['images']):
            property_image = PropertyImage.objects.create(
                property=property_obj,
                image=image,
                order=property_obj.images.count() + index
            )
            created_images.append(property_image)

        response_serializer = PropertyImageSerializer(
            created_images,
            many=True,
            context={'request': request}
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PropertyImageDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/properties/images/<image_id>/
    Deletes image from database and storage.
    """
    queryset = PropertyImage.objects.select_related('property', 'property__owner')
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        image = super().get_object()
        self.check_object_permissions(self.request, image.property)

        if image.property.owner != self.request.user:
            self.permission_denied(
                self.request,
                message='You do not have permission to delete this image.'
            )

        return image