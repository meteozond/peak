from django.test import TestCase
from django.urls import reverse

from peak.companies.models import Company
from peak.companies.tests.factories import CompanyFactory
from peak.core.tests.mixins import AddressTestMixin, APIAuthTestMixin
from peak.core.tests.utils import generate_company_data


class TestCompaniesView(AddressTestMixin, APIAuthTestMixin, TestCase):

    def setUp(self):
        self.objects_count = 5
        CompanyFactory.create_batch(self.objects_count)
        super(TestCompaniesView, self).setUp()

    def test_list(self):
        url = reverse('api:companies-list')
        response = self.client.get(url, format='json')

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Запрос не вернул обьекты БД'
        self.assertEqual(self.objects_count, response.json()['count'], message)

        self.client.logout()
        response = self.client.get(url)
        message = 'Представление только для авторизованных пользователей'
        self.assertEqual(403, response.status_code, message)

    def test_create(self):
        url = reverse('api:companies-list')
        payload = generate_company_data()
        response = self.client.post(url, data=payload, format='json')

        message = 'Invalid response status code'
        self.assertEqual(201, response.status_code, message)

        message = 'Обьект не создан'
        self.assertEqual(self.objects_count + 1, Company.objects.count(), message)

    def test_delete(self):
        company = Company.objects.select_related().first()
        url = reverse('api:companies-detail', kwargs={'pk': company.pk})
        response = self.client.delete(url, format='json')

        message = 'Invalid response status code'
        self.assertEqual(204, response.status_code, message)

        message = 'Обьект не удалился из БД'
        self.assertEqual(self.objects_count - 1, Company.objects.count(), message)

    def test_detail(self):
        company = Company.objects.select_related().first()
        url = reverse('api:companies-detail', kwargs={'pk': company.pk})
        response = self.client.get(url, format='json')

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Ответ не содержит данных обьекта'
        self.assertEqual(company.name, response.json()['name'], message)

    def test_update(self):
        company = Company.objects.select_related().first()
        old_name = company.name
        old_room = company.address.room
        payload = generate_company_data()
        url = reverse('api:companies-detail', kwargs={'pk': company.pk})
        response = self.client.put(url, data=payload, format='json')
        company.refresh_from_db()

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Обьект не обновился'
        self.assertNotEqual(old_name, company.name, message)
        self.assertNotEqual(old_room, company.address.room, message)
