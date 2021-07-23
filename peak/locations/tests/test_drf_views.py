from faker import Faker

from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from peak.core.tests.mixins import AddressTestMixin, APIAuthTestMixin
from peak.locations.models import Company, Location, LocService, Service
from peak.locations.tests.factories import (LocWithServiceFactory,
                                            ServiceFactory)

faker = Faker()


class TestLocationsAPIView(AddressTestMixin, APIAuthTestMixin, TestCase):

    def setUp(self):
        self.objects_count = 5
        LocWithServiceFactory.create_batch(self.objects_count)
        self.payload = {
            "type": "Feature",
            "geometry": Location.objects.first().location.ewkt,
            "properties": {
                "name": faker.street_address(),
                "company": Company.objects.first().id,
                "services": [
                    {
                        "service": Service.objects.first().id,
                        "price": "{}".format(faker.pyfloat(left_digits=4, right_digits=2))
                    }
                ]
            }
        }
        super(TestLocationsAPIView, self).setUp()

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
        response = self.client.post(url, data=self.payload, format='json')
        message = 'Invalid response status code'
        self.assertEqual(201, response.status_code, message)
        message = 'Обьект не создан'
        self.assertEqual(self.objects_count + 1, Location.objects.count(), message)

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
        payload['company'] = obj.company.id

        new_service_obj = ServiceFactory.create()
        new_service = payload['properties']['services'][0].copy()
        new_service['service'] = new_service_obj.id
        payload['properties']['services'].append(new_service)

        url = reverse('api:locations-detail', kwargs={'pk': obj.pk})
        response = self.client.put(url, data=payload, format='json')
        obj.refresh_from_db()

        message = 'Invalid response status code'
        self.assertEqual(200, response.status_code, message)

        message = 'Обьект не обновился'
        self.assertNotEqual(old_name, obj.name, message)

        new_service_count = LocService.objects.filter(location=obj.id).count()
        message = 'Дополнительная услуга не создалась'
        self.assertNotEqual(old_service_count, new_service_count, message)

    def test_cache(self):
        url = reverse('api:locations-list')
        loc_count = self.client.get(url, format='json').json()['count']
        self.client.post(url, data=self.payload, format='json')
        new_loc_count = self.client.get(url, format='json').json()['count']
        message = 'Инвалидация кеша не работает'
        self.assertEqual(loc_count + 1, new_loc_count, message)
