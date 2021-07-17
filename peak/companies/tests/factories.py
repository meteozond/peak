from random import randrange

from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from peak.addresses.tests.factories import AddressFactory

from ..models import Company


class CompanyFactory(DjangoModelFactory):
    name = Faker('company')
    phone = LazyAttribute(
        lambda _: str(randrange(1_000_000_00_00, 9_999_999_99_99))
    )
    address = SubFactory(AddressFactory)
    email = Faker('email')

    class Meta:
        model = Company
