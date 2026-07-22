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
            'sell_price',
            'rent_price',
            'currency',
            'total_area',
            'bedrooms',
            'bathrooms',
            'construction_year',
            'city',
            'country',
            'main_image',
            'is_premium',
            'is_featured',
            'owner_name',
            'images_count',
            'date_created',
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
            'have_documentation',
            'doc_file',
            'video_url',
            'property_type',
            'listing_type',
            'status',
            'sell_price',
            'rent_price',
            'currency',
            'total_area',
            'location',
            'city',
            'country',
            'latitude',
            'longitude',
            'main_image',
            'images',
            'is_premium',
            'is_featured',
            'is_published',
            'date_created',
            'date_updated',
            # apartment
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
            'construction_year',
            'management_fee',
            # villa
            'land_size',
            'number_of_floors',
            'basement',
            'swimming_pool',
            'security_system',
            'outdoor_extras',
            # land
            'zoning_type',
            'road_frontage',
            'terrain_topography',
            'max_allowed_floors',
            'road_access',
            'utilities',
        )
        read_only_fields = (
            'id',
            'owner',
            'date_created',
            'date_updated',
        )


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'title',
            'description',
            'have_documentation',
            'doc_file',
            'video_url',
            'property_type',
            'listing_type',
            'status',
            'sell_price',
            'rent_price',
            'currency',
            'total_area',
            'location',
            'city',
            'country',
            'latitude',
            'longitude',
            'main_image',
            'is_premium',
            'is_featured',
            'is_published',
            # apartment
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
            'construction_year',
            'management_fee',
            # villa
            'land_size',
            'number_of_floors',
            'basement',
            'swimming_pool',
            'security_system',
            'outdoor_extras',
            # land
            'zoning_type',
            'road_frontage',
            'terrain_topography',
            'max_allowed_floors',
            'road_access',
            'utilities',
        )



    def validate_total_area(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Total area must be greater than zero.')
        return value