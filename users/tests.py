from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class UserFoundationTests(TestCase):
    def test_user_ids_are_distinct_uuid4_values_and_not_editable(self):
        first = get_user_model().objects.create_user(username="uuid-first")
        second = get_user_model().objects.create_user(username="uuid-second")
        first.refresh_from_db()
        self.assertIsInstance(first.pk, uuid.UUID)
        self.assertEqual(first.pk.version, 4)
        self.assertNotEqual(first.pk, second.pk)
        self.assertFalse(get_user_model()._meta.pk.editable)

    def test_uuid_relations_permissions_and_admin_history(self):
        user = get_user_model().objects.create_user(username="uuid-relations")
        group = Group.objects.create(name="test-group")
        permission = Permission.objects.get(codename="view_user", content_type__app_label="users")
        user.groups.add(group)
        user.user_permissions.add(permission)
        log = LogEntry.objects.create(
            user=user, content_type=ContentType.objects.get_for_model(user),
            object_id=str(user.pk), object_repr="test-user", action_flag=ADDITION,
        )
        self.assertEqual(group.user_set.get().pk, user.pk)
        self.assertTrue(user.has_perm("users.view_user"))
        log.refresh_from_db()
        self.assertEqual(log.user_id, user.pk)
        self.assertEqual(log.get_edited_object(), user)

    def test_login_and_admin_change_url_with_uuid(self):
        user = get_user_model().objects.create_superuser(username="uuid-admin", password="test-password")
        self.assertTrue(self.client.login(username="uuid-admin", password="test-password"))
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
        self.assertEqual(self.client.get(reverse("admin:users_user_change", args=[user.pk])).status_code, 200)

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
import uuid

from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
