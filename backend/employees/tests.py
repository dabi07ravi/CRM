from rest_framework.test import APITestCase

from accounts.models import User


class EmployeeTestCase(APITestCase):

    def setUp(self):

        self.admin = User.objects.create(
            email="admin@gmail.com",
            role="ADMIN"
        )

        self.admin.set_password("admin123")
        self.admin.save()

        # Login Admin
        response = self.client.post(
            "/api/auth/login/",
            {
                "email": "admin@gmail.com",
                "password": "admin123"
            },
            format="json"
        )

        self.access_token = response.data["access_token"]


    def test_admin_can_create_employee(self):

        payload = {
            "first_name": "Ravindra",
            "last_name": "Dabi",
            "email": "ravindra@gmail.com"
        }

        response = self.client.post(
            "/api/employee/create/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTrue(
            User.objects.filter(
                email="ravindra@gmail.com"
            ).exists()
        )

    def test_employee_cannot_create_employee(self):

        # Create an employee
        employee = User.objects.create(
            email="employee@gmail.com",
            role="EMPLOYEE"
        )

        employee.set_password("employee123")
        employee.save()

        # Login as employee
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "employee@gmail.com",
                "password": "employee123"
            },
            format="json"
        )

        employee_token = login_response.data["access_token"]

        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com"
        }

        response = self.client.post(
            "/api/employee/create/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {employee_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            403
        )

        self.assertFalse(
            User.objects.filter(
                email="john@gmail.com"
            ).exists()
        )


    def test_duplicate_email_validation(self):

        payload = {
            "first_name": "Ravindra",
            "last_name": "Dabi",
            "email": "ravindra@gmail.com"
        }

        # First employee creation
        response = self.client.post(
            "/api/employee/create/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        # Try creating employee with same email
        response = self.client.post(
            "/api/employee/create/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            response.data["message"],
            "Validation failed"
        )

        self.assertEqual(
            str(response.data["errors"]["email"][0]),
            "user with this email already exists."
        )

        self.assertEqual(
            User.objects.filter(
                email="ravindra@gmail.com"
            ).count(),
            1
        )


    def test_employee_list_works(self):

        User.objects.create(
            email="employee1@gmail.com",
            role="EMPLOYEE"
        )

        User.objects.create(
            email="employee2@gmail.com",
            role="EMPLOYEE"
        )

        response = self.client.get(
            "/api/employee/all/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data['count'],
            2
        )

    def test_employee_detail_works(self):

        employee = User.objects.create(
            first_name="Ravindra",
            last_name="Dabi",
            email="ravindra@gmail.com",
            role="EMPLOYEE"
        )

        response = self.client.get(
            f"/api/employee/{employee.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["id"],
            employee.id
        )

        self.assertEqual(
            response.data["email"],
            "ravindra@gmail.com"
        )

        self.assertEqual(
            response.data["first_name"],
            "Ravindra"
        )

        self.assertEqual(
            response.data["last_name"],
            "Dabi"
        )

        self.assertEqual(
            response.data["role"],
            "EMPLOYEE"
        )

    def test_employee_update_works(self):

        employee = User.objects.create(
            first_name="Ravindra",
            last_name="Dabi",
            email="ravindra@gmail.com",
            role="EMPLOYEE"
        )

        payload = {
            "first_name": "Rahul",
            "last_name": "Sharma"
        }

        response = self.client.patch(
            f"/api/employee/update/{employee.id}/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        # Reload updated data from database
        employee.refresh_from_db()

        self.assertEqual(
            employee.first_name,
            "Rahul"
        )

        self.assertEqual(
            employee.last_name,
            "Sharma"
        )

        self.assertEqual(
            employee.email,
            "ravindra@gmail.com"
        )

        # Verify API response
        self.assertEqual(
            response.data["first_name"],
            "Rahul"
        )

        self.assertEqual(
            response.data["last_name"],
            "Sharma"
        )

    def test_employee_delete_works(self):

        employee = User.objects.create(
            first_name="Ravindra",
            last_name="Dabi",
            email="ravindra@gmail.com",
            role="EMPLOYEE"
        )

        response = self.client.delete(
            f"/api/employee/delete/{employee.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertFalse(
            User.objects.filter(
                id=employee.id
            ).exists()
        )