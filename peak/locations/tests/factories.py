from factory import Faker, LazyAttribute, RelatedFactory, SubFactory
from factory.django import DjangoModelFactory

from peak.companies.tests.factories import CompanyFactory
from peak.core.utils import generate_polygon
from peak.locations.models import Location, LocServices, Service


class ServiceFactory(DjangoModelFactory):
    name = Faker('bs')

    class Meta:
        model = Service


class LocationFactory(DjangoModelFactory):
    name = Faker('street_name')
    location = LazyAttribute(lambda _: generate_polygon())
    company = SubFactory(CompanyFactory)

    class Meta:
        model = Location


class LocWithServiceFactory(DjangoModelFactory):
    location = SubFactory(LocationFactory)
    service = SubFactory(ServiceFactory)
    price = Faker('pydecimal', positive=True, left_digits=6, right_digits=2)

    class Meta:
        model = LocServices
