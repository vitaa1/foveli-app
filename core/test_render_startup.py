import os
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

from django.test import SimpleTestCase


class RenderStartupTests(SimpleTestCase):
    script = Path(__file__).resolve().parent.parent / "scripts" / "start_render.py"

    def test_migrates_before_replacing_process_with_gunicorn(self):
        for port, expected in (("10000", "10000"), ("", "8000")):
            with self.subTest(port=port), patch.dict(os.environ, {"PORT": port}), \
                    patch("os.chdir"), patch("subprocess.run") as migrate, \
                    patch("os.execvp") as execute:
                def start(*args):
                    migrate.assert_called_once_with(
                        [sys.executable, "manage.py", "migrate", "--noinput"], check=True,
                    )
                execute.side_effect = start
                runpy.run_path(str(self.script), run_name="__main__")
                execute.assert_called_once_with("gunicorn", [
                    "gunicorn", "foveli.wsgi:application", "--bind",
                    f"0.0.0.0:{expected}", "--workers", "2", "--access-logfile", "-",
                ])

    def test_failed_migration_prevents_server_start(self):
        with patch("os.chdir"), patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "migrate")), \
                patch("os.execvp") as execute:
            with self.assertRaises(subprocess.CalledProcessError):
                runpy.run_path(str(self.script), run_name="__main__")
            execute.assert_not_called()
