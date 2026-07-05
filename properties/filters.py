import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_area = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='area', lookup_expr='lte')

    class Meta:
        model = Property
        fields = (
            'city',
            'property_type',
            'listing_type',
            'status',
            'bedrooms',
            'bathrooms',
            'is_featured',
        )