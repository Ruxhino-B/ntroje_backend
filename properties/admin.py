from django.contrib import admin
from django.utils.html import format_html

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    max_num = 20
    fields = (
        'image',
        'image_preview',
        'alt_text',
        'order',
        'created_at',
    )
    readonly_fields = (
        'image_preview',
        'created_at',
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="90" height="70" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Preview'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]

    list_display = (
        'title',
        'property_type',
        'listing_type',
        'status',
        'sell_price',
        'rent_price',
        'currency',
        'city',
        'construction_year',
        'owner',
        'is_premium',
        'is_featured',
        'is_published',
        'date_created',
        'main_image_preview',
    )
    list_filter = (
        'property_type',
        'listing_type',
        'status',
        'city',
        'construction_year',
        'is_premium',
        'is_featured',
        'is_published',
        'date_created',
    )
    search_fields = (
        'title',
        'description',
        'location',
        'city',
        'owner__email',
        'owner__username',
    )
    ordering = ('-is_premium', '-date_updated')
    readonly_fields = ('date_created', 'date_updated', 'main_image_preview')

    fieldsets = (
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Basic information', {
            'fields': (
                'title',
                'description',
                'have_documentation',
                'doc_file',
                'video_url',
                'property_type',
                'listing_type',
                'status',
            )
        }),
        ('Price & dimensions', {
            'fields': (
                'sell_price',
                'rent_price',
                'currency',
                'total_area',
                'construction_year',
            )
        }),
        ('Location', {
            'fields': (
                'location',
                'city',
                'country',
                'latitude',
                'longitude',
            )
        }),
        ('Media', {
            'fields': (
                'main_image',
                'main_image_preview',
            )
        }),
        ('Apartment details', {
            'fields': (
                'total_living_area',
                'bedrooms',
                'bathrooms',
                'floor',
                'balcony',
                'view',
                'elevator',
                'furnishing_status',
                'heating_colling_system',
                'parking_spots',
                'orientation',
                'total_floors',
                'management_fee',
            ),
            'classes': ('collapse',),
        }),
        ('Villa details', {
            'fields': (
                'land_size',
                'number_of_floors',
                'basement',
                'swimming_pool',
                'security_system',
                'outdoor_extras',
            ),
            'classes': ('collapse',),
        }),
        ('Land details', {
            'fields': (
                'zoning_type',
                'road_frontage',
                'terrain_topography',
                'max_allowed_floors',
                'road_access',
                'utilities',
            ),
            'classes': ('collapse',),
        }),
        ('Settings', {
            'fields': (
                'is_premium',
                'is_featured',
                'is_published',
            )
        }),
        ('Timestamps', {
            'fields': (
                'date_created',
                'date_updated',
            )
        }),
    )

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.main_image.url
            )
        return '-'

    main_image_preview.short_description = 'Main image'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'property',
        'image_preview',
        'alt_text',
        'order',
        'created_at',
    )
    list_filter = (
        'created_at',
    )
    search_fields = (
        'property__title',
        'alt_text',
    )
    ordering = (
        'property',
        'order',
        'created_at',
    )
    readonly_fields = (
        'image_preview',
        'created_at',
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="90" height="70" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Preview'