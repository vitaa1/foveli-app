from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone


class UserUUIDMigrationTests(TransactionTestCase):
    old_target = [("users", "0001_initial"), ("admin", "0003_logentry_add_action_flag_choices"), ("sessions", "0001_initial")]
    new_target = [("users", "0002_user_uuid")]

    def setUp(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.old_target)
        self.old_apps = executor.loader.project_state(self.old_target).apps
        self.addCleanup(self.restore_schema)

    def restore_schema(self):
        # Remove apenas a fixture no banco de teste antes de restaurar o schema.
        self.old_apps.get_model("sessions", "Session").objects.all().delete()
        self.old_apps.get_model("users", "User").objects.all().delete()
        MigrationExecutor(connection).migrate(self.new_target)

    def test_empty_schema_converts_user_and_foreign_keys(self):
        MigrationExecutor(connection).migrate(self.new_target)
        expected = [
            ("users_user", "id"), ("users_user_groups", "user_id"),
            ("users_user_user_permissions", "user_id"), ("django_admin_log", "user_id"),
        ]
        with connection.cursor() as cursor:
            for table, column in expected:
                cursor.execute(
                    "SELECT data_type FROM information_schema.columns "
                    "WHERE table_schema = current_schema() AND table_name = %s AND column_name = %s",
                    [table, column],
                )
                self.assertEqual(cursor.fetchone(), ("uuid",), (table, column))

    def test_populated_schema_is_blocked_without_losing_account(self):
        User = self.old_apps.get_model("users", "User")
        user = User.objects.create(username="preserve-existing-user", password="fixture-hash")
        with self.assertRaisesRegex(RuntimeError, "Nenhum dado foi apagado"):
            MigrationExecutor(connection).migrate(self.new_target)
        self.assertTrue(User.objects.filter(pk=user.pk, username=user.username).exists())

    def test_remaining_session_blocks_conversion_without_deleting_it(self):
        Session = self.old_apps.get_model("sessions", "Session")
        Session.objects.create(session_key="legacy-session", session_data="legacy", expire_date=timezone.now())
        with self.assertRaisesRegex(RuntimeError, "tabela de sessoes vazia"):
            MigrationExecutor(connection).migrate(self.new_target)
        self.assertTrue(Session.objects.filter(pk="legacy-session").exists())
