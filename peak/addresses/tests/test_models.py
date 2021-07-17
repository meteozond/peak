from django.test import TestCase

from peak.addresses.tests.factories import AddressFactory
from peak.addresses.models import Address


class TestAddress(TestCase):
    fixtures = [
        'fixtures/countries.json',
        'fixtures/regions.json',
        'fixtures/cities.json',
    ]

    def test_factory(self):
        AddressFactory.create_batch(5)
        message = 'Обьекты не создаются'
        self.assertEqual(5, Address.objects.count(), message)
