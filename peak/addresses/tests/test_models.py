from django.test import TestCase

from peak.addresses.models import Address
from peak.addresses.tests.factories import AddressFactory
from peak.core.tests.mixins import AddressTestMixin


class TestAddress(AddressTestMixin, TestCase):

    def test_factory(self):
        AddressFactory.create_batch(5)
        message = 'Обьекты не создаются'
        self.assertEqual(5, Address.objects.count(), message)
