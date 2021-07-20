from rest_framework import serializers

from peak.addresses.api.serializers import AddressSerializer
from peak.locations.api.serializers import LocationSerializer

from ..models import Company


class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer(help_text='Адрес')

    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'phone', 'address']

    def create(self, validated_data):
        return Company.s_objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Company.s_objects.update(instance=instance, **validated_data)


class CompanyWithLocationsSerializer(serializers.ModelSerializer):
    location_set = LocationSerializer(many=True)

    class Meta:
        model = Company
        fields = ['name', 'location_set']
