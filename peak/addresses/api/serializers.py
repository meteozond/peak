from rest_framework import serializers

from ..models import Address


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=50)

    class Meta:
        model = Address
        fields = ['city', 'postcode', 'street_name', 'building_number', 'room']
