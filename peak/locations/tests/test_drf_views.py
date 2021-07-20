from faker import Faker

from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from peak.core.tests.mixins import AddressTestMixin, APIAuthTestMixin
from peak.locations.api.serializers import LocationSerializer
from peak.locations.models import Location, LocService
from peak.locations.tests.factories import (LocWithServiceFactory,
                                            ServiceFactory)

faker = Faker()


class TestCompaniesView(AddressTestMixin, APIAuthTestMixin, TestCase):

    def setUp(self):
        self.objects_count = 5
        LocWithServiceFactory.create_batch(self.objects_count)

        self.payload = LocationSerializer(Location.objects.first())
        self.payload.data['id'] = 0
        self.payload.data['properties']['name'] = faker.address()

        super(TestCompaniesView, self).setUp()

    def test_list(self):
        url = reverse('api:locations-list')
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
        url = reverse('api:locations-list')

        response = self.client.post(url, data=self.payload.data, format='json')
        message = 'Invalid response status code'
        self.assertEqual(201, response.status_code, message)

        message = 'Обьект не создан'
        self.assertEqual(self.objects_count + 1, LocService.objects.count(), message)

    def test_delete(self):
        obj = Location.objects.select_related().first()
        url = reverse('api:locations-detail', kwargs={'pk': obj.pk})
        response = self.client.delete(url, format='json')

        message = 'Invalid response status code'
        self.assertEqual(204, response.status_code, message)

        message = 'Обьект не удалился из БД'
        self.assertEqual(self.objects_count - 1, Location.objects.count(), message)

    def test_detail(self):
        obj = Location.objects.select_related().first()
        url = reverse('api:locations-detail', kwargs={'pk': obj.pk})
        response = self.client.get(url, format='json')

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Ответ не содержит данных обьекта'
        self.assertEqual(obj.name, response.json()['properties']['name'], message)

    def test_update(self):
        obj = (Location.objects
               .prefetch_related('company', 'locservice_set')
               .annotate(services_count=Count('locservice'))
               .first()
               )
        old_name = obj.name
        old_service_count = obj.services_count

        payload = self.payload
        payload.data['id'] = obj.id
        new_service_obj = ServiceFactory()
        new_service = payload.data['properties']['services'][0].copy()
        new_service['service'] = new_service_obj.id
        payload.data['properties']['services'].append(new_service)

        url = reverse('api:locations-detail', kwargs={'pk': obj.pk})
        response = self.client.put(url, data=payload.data, format='json')
        obj.refresh_from_db()

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Обьект не обновился'
        self.assertNotEqual(old_name, obj.name, message)

        new_service_count = LocService.objects.filter(location=obj.id).count()
        message = 'Дополнительная услуга не создалась'
        self.assertNotEqual(old_service_count, new_service_count, message)
