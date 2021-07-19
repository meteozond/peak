from django.test import TestCase

from peak.companies.models import Company
from peak.core.tests.mixins import AddressTestMixin
from peak.locations.models import Location, Service
from peak.locations.tests.factories import LocWithServiceFactory


class TestLocation(AddressTestMixin, TestCase):

    def test_factory(self):
        num_objects = 5
        LocWithServiceFactory.create_batch(num_objects)

        message = 'Обьекты не создаются'
        self.assertEqual(num_objects, Location.objects.count(), message)
        self.assertEqual(num_objects, Service.objects.count(), message)
        self.assertEqual(num_objects, Company.objects.count(), message)
