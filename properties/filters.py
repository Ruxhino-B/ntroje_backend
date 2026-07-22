import django_filters
from django.db.models import Q

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    min_sell_price = django_filters.NumberFilter(field_name='sell_price', lookup_expr='gte')
    max_sell_price = django_filters.NumberFilter(field_name='sell_price', lookup_expr='lte')
    min_rent_price = django_filters.NumberFilter(field_name='rent_price', lookup_expr='gte')
    max_rent_price = django_filters.NumberFilter(field_name='rent_price', lookup_expr='lte')
    min_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='lte')
    owner_id = django_filters.NumberFilter(field_name='owner_id')
    owner_first_name_or_last_name = django_filters.CharFilter(method='filter_owner_name')
    construction_year_from = django_filters.NumberFilter(field_name='construction_year', lookup_expr='gte')
    construction_year_to = django_filters.NumberFilter(field_name='construction_year', lookup_expr='lte')
    agency_id = django_filters.NumberFilter(field_name='agency_id')

    def filter_owner_name(self, queryset, name, value):
        return queryset.filter(
            Q(owner__first_name__istartswith=value) | Q(owner__last_name__istartswith=value)
        )

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