from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    EMPLOYEE = "EMPLOYEE", "Employee"