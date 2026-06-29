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


    def test_login_failure(self):

        payload = {
            "email": "admin@gmail.com",
            "password": "wrongpassword"
        }

        response = self.client.post(
            "/api/auth/login/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            401
        )

        self.assertEqual(

            response.data["message"],
            "Invalid credentials"
        )

    def test_refresh_token_success(self):

    # Step 1: Login
        login_payload = {
            "email": "admin@gmail.com",
            "password": "admin123"
        }

        login_response = self.client.post(
            "/api/auth/login/",
            login_payload,
            format="json"
        )

        refresh_token = login_response.data["refresh_token"]

        # Step 2: Refresh Access Token
        response = self.client.post(
            "/api/auth/token/refresh/",
            {
                "refresh": refresh_token
            },
            format="json"
        )

        # Step 3: Assertions
        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "access",
            response.data
        )

    def test_change_password_success(self):

        # Step 1: Login
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "admin@gmail.com",
                "password": "admin123"
            },
            format="json"
        )

        access_token = login_response.data["access_token"]

        # Step 2: Change Password
        response = self.client.post(
            "/api/employee/reset_password/",
            {
                "old_password": "admin123",
                "new_password": "newpassword123"
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["message"],
            "Password changed successfully"
        )

        # Step 3: Refresh user from database
        self.user.refresh_from_db()

        self.assertFalse(
            self.user.must_change_password
        )

        # Step 4: Old password should fail
        old_login = self.client.post(
            "/api/auth/login/",
            {
                "email": "admin@gmail.com",
                "password": "admin123"
            },
            format="json"
        )

        self.assertEqual(
            old_login.status_code,
            401
        )

        # Step 5: New password should work
        new_login = self.client.post(
            "/api/auth/login/",
            {
                "email": "admin@gmail.com",
                "password": "newpassword123"
            },
            format="json"
        )

        self.assertEqual(
            new_login.status_code,
            200
        )