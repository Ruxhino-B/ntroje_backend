import os
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

from agency.models import Agency

PROPERTY_TYPE_APARTMENT = 'apartment'
PROPERTY_TYPE_HOUSE = 'house'
PROPERTY_TYPE_VILLA = 'villa'
PROPERTY_TYPE_LAND = 'land'
PROPERTY_TYPE_COMMERCIAL = 'commercial'
PROPERTY_TYPE_OFFICE = 'office'

PROPERTY_TYPE_CHOICES = (
    (PROPERTY_TYPE_APARTMENT, 'Apartment'),
    (PROPERTY_TYPE_HOUSE, 'House'),
    (PROPERTY_TYPE_VILLA, 'Villa'),
    (PROPERTY_TYPE_LAND, 'Land'),
    (PROPERTY_TYPE_COMMERCIAL, 'Commercial'),
    (PROPERTY_TYPE_OFFICE, 'Office'),
)


LISTING_TYPE_SALE = 'sale'
LISTING_TYPE_RENT = 'rent'

LISTING_TYPE_CHOICES = (
    (LISTING_TYPE_SALE, 'Sale'),
    (LISTING_TYPE_RENT, 'Rent'),
)


PROPERTY_STATUS_DRAFT = 'draft'
PROPERTY_STATUS_PUBLISHED = 'published'
PROPERTY_STATUS_SOLD = 'sold'
PROPERTY_STATUS_RENTED = 'rented'
PROPERTY_STATUS_ARCHIVED = 'archived'

PROPERTY_STATUS_CHOICES = (
    (PROPERTY_STATUS_DRAFT, 'Draft'),
    (PROPERTY_STATUS_PUBLISHED, 'Published'),
    (PROPERTY_STATUS_SOLD, 'Sold'),
    (PROPERTY_STATUS_RENTED, 'Rented'),
    (PROPERTY_STATUS_ARCHIVED, 'Archived'),
)

ZONING_TYPE_CHOICES = (
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
    ('industrial', 'Industrial'),
    ('agricultural', 'Agricultural'),
    ('mixed_use', 'Mixed Use'),
)

TERRAIN_TOPOGRAPHY_CHOICES = (
    ('flat', 'Flat'),
    ('hilly', 'Hilly'),
    ('mountainous', 'Mountainous'),
    ('valley', 'Valley'),
    ('coastal', 'Coastal'),
    ('island', 'Island'),
)

FURNISHING_STATUS_CHOICES = (
    ('fully_furnished', 'Fully Furnished'),
    ('partially_furnished', 'Partially Furnished'),
    ('unfurnished', 'Unfurnished'),
)

ROAD_ACCESS_CHOICES = (
('asphalt', 'Asphalt'),
('dirt', 'Dirt'),
('no_public_access', 'No Public Access'),
('landlocked', 'Landlocked'),
)


def property_image_upload_path(instance, filename):
    return f'properties/{filename}'


# dua te nxjerr disa statistika.
# eshte me mire te krijoj nje app te ri?
# dua te gjitha statistikat qe i duhet nje real estate ne dashboard page.
# po ashtu ne "My poperties" me duhen statistikat si publishedCount, draftCount, pandingCount, totalView

class Property(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, related_name='properties', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    have_documentation = models.BooleanField(default=False)
    doc_file = models.FileField(upload_to='documents/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    property_type = models.CharField( max_length=30, choices=PROPERTY_TYPE_CHOICES, default=PROPERTY_TYPE_APARTMENT)
    listing_type = models.CharField( max_length=20, choices=LISTING_TYPE_CHOICES, default=LISTING_TYPE_RENT)
    status = models.CharField( max_length=20, choices=PROPERTY_STATUS_CHOICES, default=PROPERTY_STATUS_DRAFT)

    sell_price = models.DecimalField(max_digits=12, decimal_places=2)
    rent_price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='EUR')
    total_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Albania')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    main_image = models.ImageField(upload_to=property_image_upload_path, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    # apartment
    total_living_area = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    floor = models.IntegerField(blank=True, null=True)
    balcony = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    view = models.CharField(max_length=250, blank=True, null=True)
    elevator = models.BooleanField(default=False)
    furnishing_status = models.CharField(max_length=100, choices=FURNISHING_STATUS_CHOICES, blank=True, null=True)
    heating_colling_system = models.CharField(max_length=100, blank=True, null=True)
    parking_spots = models.PositiveIntegerField(default=0)
    orientation = models.CharField(max_length=100, blank=True, null=True)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    construction_year = models.PositiveIntegerField(blank=True, null=True)
    management_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Villa
    land_size = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    number_of_floors = models.PositiveIntegerField(blank=True, null=True)
    basement = models.BooleanField(default=False)
    swimming_pool = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    security_system = models.BooleanField(default=False)
    outdoor_extras = models.CharField(max_length=250, blank=True, null=True)

    # Land
    zoning_type = models.CharField(max_length=100, choices=ZONING_TYPE_CHOICES, blank=True, null=True)
    road_frontage = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    terrain_topography = models.CharField(max_length=100, choices=TERRAIN_TOPOGRAPHY_CHOICES, blank=True, null=True)
    max_allowed_floors = models.PositiveIntegerField(blank=True, null=True)
    road_access = models.CharField(max_length=100, choices=ROAD_ACCESS_CHOICES, blank=True, null=True)
    utilities = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.location}, {self.city}, {self.country}'
    def img_actual_number(self):
        images = PropertyImage.objects.filter(property=self)
        return images.count()

    class Meta:
        db_table = 'properties'
        ordering = ['-is_premium', '-date_updated']


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=property_image_upload_path)
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'

    def __str__(self):
        return f'Image for {self.property.title}'

    def clean(self):
        if not self.pk and self.property.images.count() >= 20:
            raise ValidationError('A property can have a maximum of 20 images.')

    def save(self, *args, **kwargs):
        self.clean()

        old_image = None
        if self.pk:
            old_instance = PropertyImage.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.image != self.image:
                old_image = old_instance.image

        if self.image:
            self.image = self.compress_image(self.image)

        super().save(*args, **kwargs)

        if old_image:
            old_image.delete(save=False)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)

        super().delete(*args, **kwargs)

    def compress_image(self, image):
        img = Image.open(image)

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        max_size = (1200, 1200)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        output = BytesIO()
        img.save(output, format='JPEG', quality=75, optimize=True)
        output.seek(0)

        original_name = os.path.splitext(image.name)[0]
        compressed_name = f'{original_name}.jpg'

        return ContentFile(output.read(), name=compressed_name)