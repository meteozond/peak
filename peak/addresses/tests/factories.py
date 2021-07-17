from random import randrange

from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory
from cities_light.models import City

from ..models import Address


class AddressFactory(DjangoModelFactory):
    city = LazyAttribute(
        lambda _: City.objects.get(pk=randrange(1, 10))
    )
    postcode = Faker('pyint', min_value=1, max_value=999_999)
    street_name = Faker('street_name')
    building_number = Faker('building_number')
    room = LazyAttribute(lambda _: f'H{randrange(1, 100)}')

    class Meta:
        model = Address
