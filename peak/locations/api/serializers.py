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


class CompanyNameSerializer(serializers.ModelSerializer):
    # по необьяснимой причине без обьявления поля ID в POST запросе его не будет,
    # не смотря на то, что READONLY атрибута нигде нет и в GET запросах ID есть.
    id = serializers.IntegerField(
        help_text=_('ID компании'),
        label=_('ID компании'),
    )

    class Meta:
        model = Company
        fields = ['id', 'name']
        read_only_fields = ['name']

    def validate_id(self, value):
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                {'id': _('Такой компании не существует.')}
            )
        return value


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service

        fields = ['id', 'name']


class LocServicesSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = LocService
        fields = ['service', 'price', 'service_name']


class LocationSerializer(GeoFeatureModelSerializer):
    services = LocServicesSerializer(source='locservice_set', many=True)
    company = CompanyNameSerializer()
    location = serializers.CharField(
        help_text=_('Полигон'),
        label=_('Область обслуживания'),
        validators=[ValidateGeo(3)],
        max_length=200,
    )

    class Meta:
        model = Location
        fields = ['id', 'name', 'location', 'company', 'services']
        geo_field = 'location'

    def validate(self, attrs):
        attrs = super(LocationSerializer, self).validate(attrs)

        # У локации компании не можеть быть несколько одинаковых услуг.
        services = [a['service'].id for a in attrs['locservice_set']]
        if not len(services) == len(set(services)):
            raise serializers.ValidationError({
                'services': _('В области не может быть одинаковых услуг.')
            })
        company_location_exists = (Company.objects
                                   .filter(id=attrs['company']['id'])
                                   .filter(location__name=attrs['name'])
                                   .exists()
                                   )
        # Check Unique Together
        if company_location_exists:
            raise serializers.ValidationError({
                'name': _('У данной компании уже есть область с таким именем.')
            })

        return attrs

    def create(self, validated_data):
        services = validated_data.pop('locservice_set')
        company = Company.objects.get(id=validated_data.pop('company')['id'])
        location = Location.objects.create(company=company, **validated_data)
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
