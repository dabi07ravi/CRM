from rest_framework.test import APITestCase
from django.urls import reverse

from accounts.models import User


class LoginTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(
        email="admin@gmail.com",
        role="ADMIN"
        )

        self.user.set_password("admin123")
        self.user.save()

    def test_login_success(self):

        payload = {
            "email": "admin@gmail.com",
            "password": "admin123"
        }

        response = self.client.post(
            "/api/auth/login/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )