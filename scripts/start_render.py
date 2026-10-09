"""Inicializacao da instancia unica de testes no Render Free."""
import os
from pathlib import Path
import subprocess
import sys


def main():
    os.chdir(Path(__file__).resolve().parent.parent)
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
    os.execvp("gunicorn", [
        "gunicorn", "foveli.wsgi:application", "--bind",
        f"0.0.0.0:{os.environ.get('PORT') or '8000'}",
        "--workers", "2", "--access-logfile", "-",
    ])


if __name__ == "__main__":
    main()
