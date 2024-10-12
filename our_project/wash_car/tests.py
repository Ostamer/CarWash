
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APIClient

class AuthMiddlewareTest(TestCase):

    @override_settings(MIDDLEWARE=[])
    def test_middleware_disabled(self):
        client = APIClient()
        response = client.get(reverse('car-wash-list'))
        self.assertEqual(response.status_code, 200)