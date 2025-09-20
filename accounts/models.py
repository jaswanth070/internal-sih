from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CONTROLLER = "controller", "Section Controller"
        SUPERVISOR = "supervisor", "Supervisor"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.CONTROLLER)
    section = models.CharField(max_length=64, blank=True, help_text="Railway section code or name")

    def __str__(self):
        return f"{self.username} ({self.role})"
