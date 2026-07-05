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
        'price',
        'currency',
        'city',
        'construction_year',
        'owner',
        'is_featured',
        'is_active',
        'created_at',
        'main_image_preview',
    )
    list_filter = (
        'property_type',
        'listing_type',
        'status',
        'city',
        'construction_year',
        'is_featured',
        'is_active',
        'created_at',
    )
    search_fields = (
        'title',
        'description',
        'address',
        'city',
        'owner__email',
        'owner__username',
    )
    ordering = ('-created_at',)
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'main_image_preview')

    fieldsets = (
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Basic information', {
            'fields': (
                'title',
                'description',
                'property_type',
                'listing_type',
                'status',
            )
        }),
        ('Price & dimensions', {
            'fields': (
                'price',
                'currency',
                'area',
                'bedrooms',
                'bathrooms',
                'floor',
                'total_floors',
                'construction_year',
            )
        }),
        ('Location', {
            'fields': (
                'address',
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
        ('Settings', {
            'fields': (
                'is_featured',
                'is_active',
                'views_count',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
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