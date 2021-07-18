from django.test import TestCase
from rest_framework.test import APIClient
from peak.core.tests.utils import create_user


class AddressTestMixin:
    """
    Заполнение тестовой базы адресов небольшими фикстурами.
    """
    fixtures = [
        'fixtures/countries.json',
        'fixtures/regions.json',
        'fixtures/cities.json',
    ]


class APIAuthTestMixin(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user, self.user_password = create_user()
        self.client.login(username=self.user, password=self.user_password)
