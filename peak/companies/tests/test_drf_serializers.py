from cities_light.models import City

from django.test import TestCase

from peak.addresses.tests.factories import AddressFactory
from peak.companies.api.serializers import CompanySerializer
from peak.companies.models import Company
from peak.companies.tests.factories import CompanyFactory
from peak.core.tests.mixins import AddressTestMixin
from peak.core.utils import generate_phone_number, get_factory_data


class TestCompanySerializer(AddressTestMixin, TestCase):

    def get_initial_data(self):
        """
        Генерирует данные для инициализации сериализатора.
        """
        address_data = get_factory_data(AddressFactory)
        address_data['city'] = City.objects.first().name

        company_data = get_factory_data(CompanyFactory)
        company_data['address'] = address_data
        company_data['phone'] = generate_phone_number()
        return company_data

    def test_create(self):
        serializer = CompanySerializer(data=self.get_initial_data())
        message = 'Сериализатор не принимает валидные значения'
        self.assertTrue(serializer.is_valid(), message)
        serializer.save()
        message = 'Метод create не создает обьекты в БД'
        self.assertEqual(1, Company.objects.count(), message)

    def test_update(self):
        data = self.get_initial_data()
        serializer = CompanySerializer(data=data)
        serializer.is_valid()
        instance = serializer.save()

        data['address']['room'] = '666'
        data['name'] = 'Peak'
        serializer.update(instance, data)

        message = 'Сериализатор не обновил значения в БД'
        company_instance = Company.objects.select_related().first()
        self.assertEqual(data['address']['room'], company_instance.address.room, message)
        self.assertEqual(data['name'], company_instance.name, message)



