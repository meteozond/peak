from django.db.utils import IntegrityError
from django.test import TestCase

from peak.companies.models import Company
from peak.companies.tests.factories import CompanyFactory
from peak.core.tests.mixins import AddressTestMixin


class TestAddress(AddressTestMixin, TestCase):

    def test_factory(self):
        CompanyFactory.create_batch(5)
        message = 'Обьекты не создаются'
        self.assertEqual(5, Company.objects.count(), message)

    def test_CICharField(self):
        name = 'Peak'
        CompanyFactory.create(name=name)
        message = 'Сравнение должно быть регистронезависимым'
        self.assertEqual(
            Company.objects.get(name=name.lower()).name, name, message
        )
        message = 'Позволяет создавать одинаковые значения'
        with self.assertRaises(IntegrityError, msg=message):
            CompanyFactory.create(name=name.upper())
