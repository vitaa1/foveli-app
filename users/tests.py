from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class UserFoundationTests(TestCase):
    def test_regular_user_has_no_admin_access(self):
        user = get_user_model().objects.create_user(username="vendedor", password="test-password")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("test-password"))
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)

    def test_inactive_user_cannot_login(self):
        get_user_model().objects.create_user(username="inativo", password="test-password", is_active=False)
        self.assertFalse(self.client.login(username="inativo", password="test-password"))

    def test_superuser_can_access_admin(self):
        user = get_user_model().objects.create_superuser(username="dono", password="test-password")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 200)

    def test_deactivated_user_loses_existing_session_access(self):
        user = get_user_model().objects.create_superuser(username="desativado", password="test-password")
        self.client.force_login(user)
        user.is_active = False
        user.save(update_fields=["is_active"])
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)

    def test_admin_login_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("admin:login"), {"username": "dono", "password": "test-password"})
        self.assertEqual(response.status_code, 403)
