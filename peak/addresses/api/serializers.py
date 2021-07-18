from rest_framework import serializers

from ..models import Address
from ..validators import validate_city


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=50, validators=[validate_city, ])

    class Meta:
        model = Address
        fields = ['city', 'postcode', 'street_name', 'building_number', 'room']
