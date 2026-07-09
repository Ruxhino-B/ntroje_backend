import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    min_sell_price = django_filters.NumberFilter(field_name='sell_price', lookup_expr='gte')
    max_sell_price = django_filters.NumberFilter(field_name='sell_price', lookup_expr='lte')
    min_rent_price = django_filters.NumberFilter(field_name='rent_price', lookup_expr='gte')
    max_rent_price = django_filters.NumberFilter(field_name='rent_price', lookup_expr='lte')
    min_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='lte')

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
            'is_premium',
            'is_published',
        )