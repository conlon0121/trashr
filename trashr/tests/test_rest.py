from _decimal import Decimal

from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.test import APITestCase

from trashr.models import IntervalReading, Dumpster, Organization

class TestRest(APITestCase):
    def setUp(self):
        Organization.objects.create(name="1", email='conlon0121@gmail.com')
        coords = [Decimal(1), Decimal(1)]
        Dumpster.objects.create(core_id='36005a000551353431383736',
                                capacity=100, coordinates=coords)
        self.adminuser = User.objects.create(username='adminuser', password='adminpass',
                                             email='email@test.com',
                                             is_staff=True)
        self.client.force_authenticate(user=self.adminuser)

    def test_create_reading(self):
        test_data = {
            "name": "production",
            "data": "{\"readings\": [20, 20, 20], \"reading_attempts\": 4}",
            "ttl": 60,
            "published_at": "2017-11-04T03:58:40.379Z",
            "coreid": "36005a000551353431383736"
        }
        self.client.post(reverse('create'), data=test_data, format='json')
        self.assertEqual(1, IntervalReading.objects.count())
        self.assertEqual(3, len(IntervalReading.objects.first().raw_readings))
