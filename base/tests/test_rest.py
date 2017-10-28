from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.test import APITestCase

from base.models import IntervalReading, Dumpster, Organization


class TestRest(APITestCase):
    def setUp(self):
        Organization.objects.create(name="1")
        dumpster = Dumpster.objects.create(id=1, capacity=100)
        self.adminuser = User.objects.create(username='adminuser', password='adminpass',
                                             email='email@test.com',
                                             is_staff=True)
        self.client.force_authenticate(user=self.adminuser)

    def test_create_reading(self):
        test_data = {'event': ['local_test'],
                     'data': "{'dumpster': 1, 'readings': [-1, 154, 154]}",
                     'published_at': '2017-10-28T20:02:43.525Z',
                     'coreid': ['api']}
        self.client.post(reverse('create'), data=test_data, format='json')
        self.assertEqual(3, IntervalReading.objects.count())
        self.assertEqual(1, IntervalReading.objects.first().dumpster.id)

