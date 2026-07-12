from rest_framework import serializers

from accounts.serializers import UserMeSerializer
from .models import Agency, AgencyMember


class AgencyMiniSerializer(serializers.ModelSerializer):
    """Lightweight serializer — used nested inside other serializers (e.g. Property)."""

    class Meta:
        model = Agency
        fields = ('id', 'name')


class AgencyMemberSerializer(serializers.ModelSerializer):
    user = UserMeSerializer(read_only=True)

    class Meta:
        model = AgencyMember
        fields = ('id', 'agency', 'user', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class AgencyMemberCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyMember
        fields = ('id', 'agency', 'user', 'is_active')
        read_only_fields = ('id',)


class AgencyListSerializer(serializers.ModelSerializer):
    owner = UserMeSerializer(read_only=True)

    class Meta:
        model = Agency
        fields = (
            'id', 'owner', 'name', 'slug', 'logo', 'cover_image',
            'email', 'phone', 'website', 'city', 'country',
            'is_verified', 'is_active', 'date_created',
        )
        read_only_fields = ('id', 'slug', 'date_created')


class AgencyDetailSerializer(serializers.ModelSerializer):
    owner = UserMeSerializer(read_only=True)
    members = AgencyMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Agency
        fields = (
            'id', 'owner', 'name', 'slug', 'description', 'logo', 'cover_image',
            'email', 'phone', 'website', 'address', 'city', 'country',
            'is_verified', 'is_active', 'date_created', 'date_updated', 'members',
        )
        read_only_fields = ('id', 'slug', 'date_created', 'date_updated')


class AgencyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = (
            'id', 'name', 'description', 'logo', 'cover_image',
            'email', 'phone', 'website', 'address', 'city', 'country',
            'is_active',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)