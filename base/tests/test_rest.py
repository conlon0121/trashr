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
        test_data =  {'event': 'local_test',
                      'data': '{"data":"{\'dumpster\': 1,'
                              ' \'readings\': [1, 23, 157],'
                              ' \'reading_attempts\': 1}",'
                              '"ttl":60,'
                              '"published_at":"2017-10-28T17:07:35.057Z",'
                              '"coreid":"36005a000551353431383736",'
                              '"name":"production"}',
                      'published_at': '2017-10-28T18:22:29.751Z',
                      'coreid': 'api'}
        self.client.post(reverse('create'), data=test_data, format='json')
        self.assertEqual(3, IntervalReading.objects.count())
        self.assertEqual(1, IntervalReading.objects.first().dumpster.id)

