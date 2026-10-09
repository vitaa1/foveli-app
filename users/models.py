from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField("telefone", max_length=30, blank=True)

    # Administrador usa is_staff; vendedor e usuario sem acesso ao admin.
    # Regras de acesso do negocio serao implementadas no incremento seguinte.
