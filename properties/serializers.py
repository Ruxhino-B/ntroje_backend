from rest_framework import serializers

from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = (
            'id',
            'image',
            'alt_text',
            'order',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class PropertyImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False,
        max_length=20
    )

    def validate_images(self, images):
        property_obj = self.context['property']
        existing_images_count = property_obj.images.count()

        if existing_images_count + len(images) > 20:
            raise serializers.ValidationError(
                f'You can upload maximum 20 images per property. '
                f'This property already has {existing_images_count} images.'
            )

        return images


class PropertyListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    images_count = serializers.IntegerField(source='images.count', read_only=True)

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'property_type',
            'listing_type',
            'status',
            'price',
            'currency',
            'area',
            'bedrooms',
            'bathrooms',
            'construction_year',
            'city',
            'country',
            'main_image',
            'is_featured',
            'owner_name',
            'images_count',
            'created_at',
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = (
            'id',
            'owner',
            'owner_name',
            'owner_email',
            'owner_phone',
            'title',
            'description',
            'property_type',
            'listing_type',
            'status',
            'price',
            'currency',
            'area',
            'bedrooms',
            'bathrooms',
            'floor',
            'total_floors',
            'construction_year',
            'address',
            'city',
            'country',
            'latitude',
            'longitude',
            'main_image',
            'images',
            'is_featured',
            'is_active',
            'views_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'owner',
            'views_count',
            'created_at',
            'updated_at',
        )


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'title',
            'description',
            'property_type',
            'listing_type',
            'status',
            'price',
            'currency',
            'area',
            'bedrooms',
            'bathrooms',
            'floor',
            'total_floors',
            'construction_year',
            'address',
            'city',
            'country',
            'latitude',
            'longitude',
            'main_image',
            'is_featured',
            'is_active',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value

    def validate_area(self, value):
        if value <= 0:
            raise serializers.ValidationError('Area must be greater than zero.')
        return value