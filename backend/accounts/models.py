from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import UserRole


class User(AbstractUser):

    username = None


    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE
    )

    must_change_password = models.BooleanField(default=True)

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email