from decimal import Decimal

from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.test import APITestCase

from trashr.models import IntervalReading, Dumpster, Organization


class TestRest(APITestCase):
    def setUp(self):
        Organization.objects.create(name="1", email='conlon0121@gmail.com')
        coords = [Decimal(1), Decimal(1)]
        Dumpster.objects.create(core_id='470053001951353339373130',
                                capacity=100, coordinates=coords, alert_percentage=60)
        self.adminuser = User.objects.create(username='adminuser', password='adminpass',
                                             email='email@test.com',
                                             is_staff=True)
        self.client.force_authenticate(user=self.adminuser)

    def test_create_reading(self):
        test_data = {
            "name": "production",
            "data": "{\"readings\": [8]}",
            "ttl": 60,
            "published_at": "2018-01-29T14:58:33.046Z",
            "coreid": "470053001951353339373130"
        }

        self.client.post(reverse('create'), data=test_data, format='json')
        self.assertEqual(1, IntervalReading.objects.count())
        self.assertEqual(8, IntervalReading.objects.first().raw_readings[0])
        self.assertEqual(92, Dumpster.objects.first().percent_fill)
