"""Troca de PK no inicio do projeto, somente em banco sem usuarios."""
import uuid

from django.db import migrations, models


def require_empty_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    if User.objects.using(schema_editor.connection.alias).exists():
        raise RuntimeError(
            "A troca de ID para UUID exige a tabela de usuarios vazia. "
            "Nenhum dado foi apagado. Prepare uma migracao de dados antes de continuar."
        )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("admin", "0003_logentry_add_action_flag_choices"),
    ]

    operations = [
        migrations.RunPython(require_empty_users, migrations.RunPython.noop),
        # PostgreSQL nao converte bigint diretamente para uuid. O estado textual
        # intermediario permite ao Django atualizar tambem as FKs e tabelas M2M.
        migrations.AlterField(
            model_name="user", name="id",
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user", name="id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        # Reversao tambem so e segura enquanto nao houver usuarios UUID.
        migrations.RunPython(migrations.RunPython.noop, require_empty_users),
    ]
