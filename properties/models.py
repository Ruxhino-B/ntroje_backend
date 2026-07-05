import os
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


class PropertyType(models.TextChoices):
    APARTMENT = 'apartment', 'Apartment'
    HOUSE = 'house', 'House'
    VILLA = 'villa', 'Villa'
    LAND = 'land', 'Land'
    COMMERCIAL = 'commercial', 'Commercial'
    OFFICE = 'office', 'Office'


class ListingType(models.TextChoices):
    SALE = 'sale', 'Sale'
    RENT = 'rent', 'Rent'


class PropertyStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    SOLD = 'sold', 'Sold'
    RENTED = 'rented', 'Rented'
    ARCHIVED = 'archived', 'Archived'


class Property(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    property_type = models.CharField(
        max_length=30,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT
    )
    listing_type = models.CharField(
        max_length=20,
        choices=ListingType.choices,
        default=ListingType.SALE
    )
    status = models.CharField(
        max_length=20,
        choices=PropertyStatus.choices,
        default=PropertyStatus.DRAFT
    )

    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='EUR')

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Area in square meters'
    )
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    floor = models.IntegerField(blank=True, null=True)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    construction_year = models.PositiveIntegerField(blank=True, null=True)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Albania')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)


def property_image_upload_path(instance, filename):
    return f'properties/{instance.property_id}/images/{filename}'


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

        max_size = (1600, 1600)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        output = BytesIO()
        img.save(output, format='JPEG', quality=75, optimize=True)
        output.seek(0)

        original_name = os.path.splitext(image.name)[0]
        compressed_name = f'{original_name}.jpg'

        return ContentFile(output.read(), name=compressed_name)