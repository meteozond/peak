from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from peak.addresses.tests.factories import AddressFactory
from peak.core.utils import generate_phone_number

from ..models import Company


class CompanyFactory(DjangoModelFactory):
    name = Faker('company')
    phone = LazyAttribute(
        lambda _: generate_phone_number()
    )
    address = SubFactory(AddressFactory)
    email = Faker('email')

    class Meta:
        model = Company
