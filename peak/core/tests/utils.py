from faker import Faker

from cities_light.models import City

from peak.users.tests.factories import UserFactory
from peak.companies.tests.factories import CompanyFactory
from peak.addresses.tests.factories import AddressFactory

from ..utils import get_factory_data, generate_phone_number


def create_user():
    """
    Возвращает обьект пользователя и его пароль.
    """
    faker = Faker()
    password = faker.password()
    user = UserFactory.create(password=password)
    return user, password


def generate_company_data():
    """
    Генерирует данные для создания компании.
    """
    company_data = get_factory_data(CompanyFactory)
    company_data['phone'] = generate_phone_number()
    company_data['address'] = get_factory_data(AddressFactory)
    company_data['address']['city'] = City.objects.first().name
    return company_data
