"""Valida ambientes em processos isolados, sem herdar segredos do host."""
import json
import os
from pathlib import Path
import subprocess
import sys

from django.test import SimpleTestCase


class EnvironmentSettingsTests(SimpleTestCase):
    def load_settings(self, **overrides):
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
            "DJANGO_SECRET_KEY": "test-only-key-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "DJANGO_ALLOWED_HOSTS": "example.test",
        }
        environment.update(overrides)
        result = subprocess.run(
            [sys.executable, "-c", (
                "import json; from foveli import settings as s; "
                "names = ['DEBUG', 'ALLOWED_HOSTS', 'DATABASES', 'SESSION_COOKIE_SECURE', "
                "'CSRF_COOKIE_SECURE', 'SECURE_SSL_REDIRECT', 'SECURE_PROXY_SSL_HEADER']; "
                "print(json.dumps({n: getattr(s, n, None) for n in names}))"
            )],
            cwd=Path(__file__).resolve().parent.parent,
            env=environment, capture_output=True, text=True, timeout=10,
        )
        return result

    def test_production_defaults_are_secure_and_proxy_is_opt_in(self):
        result = self.load_settings()
        self.assertEqual(result.returncode, 0, result.stderr)
        settings = json.loads(result.stdout)
        self.assertFalse(settings["DEBUG"])
        for name in ("SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE", "SECURE_SSL_REDIRECT"):
            self.assertTrue(settings[name])
        self.assertIsNone(settings["SECURE_PROXY_SSL_HEADER"])

    def test_development_key_is_rejected_in_production(self):
        result = self.load_settings(DJANGO_SECRET_KEY="local-development-" + "x" * 60)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ImproperlyConfigured", result.stderr)

    def test_short_key_is_rejected_in_production(self):
        result = self.load_settings(DJANGO_SECRET_KEY="short")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ImproperlyConfigured", result.stderr)

    def test_database_url_overrides_local_fields_and_decodes_credentials(self):
        result = self.load_settings(
            DATABASE_URL="postgresql://some%40user:test%2Fpassword@database.test:5433/app%2Ddb?sslmode=require",
            POSTGRES_HOST="wrong-host", POSTGRES_DB="wrong-db",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        database = json.loads(result.stdout)["DATABASES"]["default"]
        self.assertEqual(database["HOST"], "database.test")
        self.assertEqual(database["PORT"], 5433)
        self.assertEqual(database["NAME"], "app-db")
        self.assertEqual(database["USER"], "some@user")
        self.assertEqual(database["PASSWORD"], "test/password")
        self.assertEqual(database["OPTIONS"]["sslmode"], "require")

    def test_explicit_sslmode_takes_precedence(self):
        result = self.load_settings(
            DATABASE_URL="postgresql://user:password@database.test/app?sslmode=require",
            POSTGRES_SSLMODE="verify-full",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["DATABASES"]["default"]["OPTIONS"]["sslmode"], "verify-full")

    def test_database_url_rejects_non_postgresql_and_missing_database(self):
        for url in ("sqlite:///tmp/test.db", "postgresql://database.test/"):
            with self.subTest(url=url):
                result = self.load_settings(DATABASE_URL=url)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ImproperlyConfigured", result.stderr)

    def test_trusted_proxy_and_host_list_are_explicit(self):
        result = self.load_settings(
            DJANGO_TRUST_PROXY="true", DJANGO_ALLOWED_HOSTS="example.test, localhost, ",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        settings = json.loads(result.stdout)
        self.assertEqual(settings["SECURE_PROXY_SSL_HEADER"], ["HTTP_X_FORWARDED_PROTO", "https"])
        self.assertEqual(settings["ALLOWED_HOSTS"], ["example.test", "localhost"])
