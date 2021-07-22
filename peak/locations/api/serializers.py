from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from django.utils.translation import gettext_lazy as _

from peak.companies.models import Company

from ..models import Location, LocService, Service
from .validators import ValidateGeo


class GeofilterSerializer(serializers.Serializer):
    """
    Для валидации и приведения к нужным типам в запросе выборки.
    """
    point = serializers.CharField(
        help_text=_('Название услуги'),
        label=_('Услуга'),
        validators=[ValidateGeo(0), ],
        allow_blank=True,
    )
    service = serializers.CharField(
        help_text=_('Название услуги'),
        label=_('Услуга'),
        max_length=100,
        allow_blank=True,
    )

    class Meta:
        fields = ['point', 'service']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']


class LocServiceListSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = LocService
        fields = ['service', 'service_name', 'price']


class LocationSerializer(GeoFeatureModelSerializer):
    services = LocServiceListSerializer(source='locservice_set', many=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'location', 'company', 'services']
        geo_field = 'location'

    @staticmethod
    def validate_location(value):
        ValidateGeo(3)(value)
        return value

    def create(self, validated_data):
        services = validated_data.pop('locservice_set')
        location = Location.objects.create(company=validated_data.pop('company'), **validated_data)
        services = [LocService(location=location, **service) for service in services]
        LocService.objects.bulk_create(services)
        return location

    def update(self, instance, validated_data):
        instance.company = validated_data.pop('company')
        instance.name = validated_data['name']
        services = validated_data['locservice_set']
        services_to_set = []
        for s in services:
            service, _ = LocService.objects.update_or_create(
                location=instance, service=s['service'], defaults={'price': s['price']}
            )
            services_to_set.append(service)
        instance.locservice_set.set(services_to_set)
        instance.locservice_set.exclude(id__in=[s.id for s in services_to_set]).delete()
        instance.save()
        return instance


class LocationListSerializer(GeoFeatureModelSerializer):
    company = CompanySerializer()
    services = LocServiceListSerializer(source='locservice_set', many=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'company', 'services']
        geo_field = 'location'
