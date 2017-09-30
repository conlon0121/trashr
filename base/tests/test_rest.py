import requests
import os

from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse

from rest_framework.test import APITestCase

from base.views import CreateReading
from base.models import IntervalReading, Dumpster, Organization, IntervalSet


class TestRest(APITestCase):
    def setUp(self):
        Organization.objects.create(name="1")
        dumpster = Dumpster.objects.create(id=1, capacity=100)
        self.adminuser = User.objects.create(username='adminuser', password='adminpass',
                                             email='email@test.com',
                                             is_staff=True)
        self.client.force_authenticate(user=self.adminuser)

    def test_create_reading(self):
        test_data = {'data' : "{'dumpster': 1,'readings': [(34, 50), (52, 60), (72, 70)]}",'ttl':60,
        "published_at":"2017-09-16T17:56:11.458Z","coreid":"api","name":"local_test"}
        self.client.post(reverse('create'), data=test_data, format='json')
        self.assertEqual(3, IntervalReading.objects.count())
        self.assertEqual(1, IntervalSet.objects.count())
        reading = IntervalReading.objects.first()
        int_set = IntervalSet.objects.first()
        self.assertAlmostEqual(71, int(reading.percent_fill))
        self.assertEqual(1, int_set.dumpster.id)

