from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from django.utils.translation import gettext_lazy as _

from ..models import Location, LocService, Service
from .validators import validate_poly


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']


class LocServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocService
        fields = ['service', 'price']


class LocationSerializer(GeoFeatureModelSerializer):
    services = LocServicesSerializer(source='locservice_set', many=True)
    location = serializers.CharField(
        help_text=_('Полигон'),
        label=_('Область обслуживания'),
        validators=[validate_poly, ],
        max_length=200,
    )

    class Meta:
        model = Location
        fields = ['id', 'name', 'location', 'company', 'services']
        geo_field = 'location'

    def validate(self, attrs):
        attrs = super(LocationSerializer, self).validate(attrs)

        services = [a['service'].id for a in attrs['locservice_set']]
        if not len(services) == len(set(services)):
            raise serializers.ValidationError({
                'services': _('В области не может быть одинаковых услуг.')
            })
        return attrs

    def create(self, validated_data):
        services = validated_data.pop('locservice_set')
        location = Location.objects.create(**validated_data)
        services = [LocService(location=location, **service) for service in services]
        LocService.objects.bulk_create(services)
        return location

    def update(self, instance, validated_data):
        services = validated_data.pop('locservice_set')
        for s in services:
            LocService.objects.update_or_create(
                location=instance, service=s['service'], defaults={'price': s['price']}
            )

        instance.name = validated_data['name']
        instance.location = validated_data['location']
        instance.save()
        return instance
