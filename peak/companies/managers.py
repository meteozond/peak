from cities_light.models import City

from django.db.models import Model, QuerySet

from peak.addresses.models import Address


class CompanyManager(QuerySet):
    pass


class CompanySerializerManager(QuerySet):

    def create(self, **kwargs) -> Model:
        address = kwargs.pop('address')
        city = City.objects.get(name=address.pop('city'))
        address = Address.objects.create(city=city, **address)
        return super(CompanySerializerManager, self).create(address=address, **kwargs)

    def update(self, instance: Model, **kwargs) -> Model:
        address = kwargs.pop('address')
        city = City.objects.get(name=address.pop('city'))
        Address.objects.filter(company=instance).update(city=city, **address)
        super(CompanySerializerManager, self).update(**kwargs)
        instance.refresh_from_db()
        return instance

