from unittest.mock import patch
from django.db import OperationalError
from django.test import TestCase
from django.urls import reverse


class HealthTests(TestCase):
    def test_health_checks_real_database(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_database_failure_does_not_expose_details(self):
        with patch("core.views.connection.cursor", side_effect=OperationalError("secret database details")):
            response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
