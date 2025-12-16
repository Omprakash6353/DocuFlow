from django.test import TestCase
import requests
from django.conf import settings

class IntegrationTest(TestCase):
    def test_fastapi_health(self):
        response = requests.get(f"{settings.FASTAPI_URL}/health/")
        self.assertEqual(response.status_code, 200)
