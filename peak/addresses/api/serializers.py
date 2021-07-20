from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from ..models import Address
from ..validators import validate_city


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(
        max_length=50,
        validators=[validate_city, ],
        label=_('Город'),
        help_text=_('Город (например, Bratsk. Лучше на английском, не было времени '
                    'разбираться с cities-light'),
    )

    class Meta:
        model = Address
        fields = ['city', 'postcode', 'street_name', 'building_number', 'room']
