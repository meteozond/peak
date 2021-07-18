from django.test import TestCase

from peak.companies.api.serializers import CompanySerializer
from peak.companies.models import Company
from peak.core.tests.mixins import AddressTestMixin
from peak.core.tests.utils import generate_company_data


class TestCompanySerializer(AddressTestMixin, TestCase):

    def test_create(self):
        serializer = CompanySerializer(data=generate_company_data())
        message = 'Сериализатор не принимает валидные значения'
        self.assertTrue(serializer.is_valid(), message)
        serializer.save()
        message = 'Метод create не создает обьекты в БД'
        self.assertEqual(1, Company.objects.count(), message)

    def test_update(self):
        data = generate_company_data()
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
