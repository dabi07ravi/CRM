from rest_framework.test import APITestCase

from accounts.models import User
from tasks.models import Task


from tasks.choices import TaskStatus


class TaskTestCase(APITestCase):

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


    def test_create_task(self):

        payload = {
            "title": "Login API",
            "description": "Create login API using JWT"
        }

        response = self.client.post(
            "/api/task/create/",
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertEqual(
            Task.objects.count(),
            1
        )

        task = Task.objects.first()

        self.assertEqual(
            task.title,
            "Login API"
        )

        self.assertEqual(
            task.description,
            "Create login API using JWT"
        )

        self.assertEqual(
            task.created_by,
            self.admin
        )

        self.assertIsNone(
            task.assigned_to
        )

        self.assertEqual(
            task.status,
            TaskStatus.PENDING
        )

    def test_assign_task(self):

    # Create Employee
        employee = User.objects.create(
            first_name="Ravindra",
            last_name="Dabi",
            email="employee@gmail.com",
            role="EMPLOYEE"
        )

        # Create Task
        task = Task.objects.create(
            title="Login API",
            description="Create login API",
            created_by=self.admin
        )

        response = self.client.patch(
            f"/api/task/{task.id}/assign/",
            {
                "employee_id": employee.id
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        # Reload task from DB
        task.refresh_from_db()

        self.assertEqual(
            task.assigned_to,
            employee
        )

        self.assertEqual(
            task.created_by,
            self.admin
        )

        self.assertEqual(
            task.status,
            TaskStatus.PENDING
        )

        self.assertEqual(
            response.data["message"],
            "Task assigned successfully"
        )

    def test_update_task_status(self):

        # Create Employee
        employee = User.objects.create(
            email="employee@gmail.com",
            role="EMPLOYEE"
        )
        employee.set_password("employee123")
        employee.save()

        # Login Employee
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "employee@gmail.com",
                "password": "employee123"
            },
            format="json"
        )

        employee_token = login_response.data["access_token"]

        # Create Task
        task = Task.objects.create(
            title="Login API",
            description="Create Login API",
            created_by=self.admin,
            assigned_to=employee
        )

        response = self.client.patch(
            f"/api/task/{task.id}/status/",
            {
                "status": "IN_PROGRESS"
            },
            HTTP_AUTHORIZATION=f"Bearer {employee_token}",
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        task.refresh_from_db()

        self.assertEqual(
            task.status,
            TaskStatus.IN_PROGRESS
        )

        self.assertEqual(
            response.data["message"],
            "Task status updated successfully"
        )

    def test_delete_task(self):

        task = Task.objects.create(
            title="Login API",
            description="Create Login API",
            created_by=self.admin
        )

        response = self.client.delete(
            f"/api/task/delete/{task.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertFalse(
            Task.objects.filter(
                id=task.id
            ).exists()
        )
        

    def test_my_tasks(self):

        employee1 = User.objects.create(
            email="employee1@gmail.com",
            role="EMPLOYEE"
        )
        employee1.set_password("employee123")
        employee1.save()

        employee2 = User.objects.create(
            email="employee2@gmail.com",
            role="EMPLOYEE"
        )
        employee2.set_password("employee123")
        employee2.save()

        task1 = Task.objects.create(
            title="Login API",
            description="Task 1",
            created_by=self.admin,
            assigned_to=employee1
        )

        task2 = Task.objects.create(
            title="JWT API",
            description="Task 2",
            created_by=self.admin,
            assigned_to=employee1
        )

        task3 = Task.objects.create(
            title="Dashboard",
            description="Task 3",
            created_by=self.admin,
            assigned_to=employee2
        )

        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "employee1@gmail.com",
                "password": "employee123"
            },
            format="json"
        )

        employee_token = login_response.data["access_token"]

        response = self.client.get(
            "/api/task/my_tasks/",
            HTTP_AUTHORIZATION=f"Bearer {employee_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            2
        )

        titles = [
            task["title"]
            for task in response.data
        ]

        self.assertIn(
            "Login API",
            titles
        )

        self.assertIn(
            "JWT API",
            titles
        )

        self.assertNotIn(
            "Dashboard",
            titles
        )

    def test_assigned_employee_can_view_task(self):

        employee = User.objects.create(
            email="employee@gmail.com",
            role="EMPLOYEE"
        )
        employee.set_password("employee123")
        employee.save()

        task = Task.objects.create(
            title="Login API",
            description="Create Login API",
            created_by=self.admin,
            assigned_to=employee
        )

        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "employee@gmail.com",
                "password": "employee123"
            },
            format="json"
        )

        employee_token = login_response.data["access_token"]

        response = self.client.get(
            f"/api/task/{task.id}/",
            HTTP_AUTHORIZATION=f"Bearer {employee_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["title"],
            "Login API"
        )

    def test_employee_cannot_view_other_employee_task(self):

        employee1 = User.objects.create(
            email="employee1@gmail.com",
            role="EMPLOYEE"
        )
        employee1.set_password("employee123")
        employee1.save()

        employee2 = User.objects.create(
            email="employee2@gmail.com",
            role="EMPLOYEE"
        )
        employee2.set_password("employee123")
        employee2.save()

        task = Task.objects.create(
            title="Login API",
            description="Create Login API",
            created_by=self.admin,
            assigned_to=employee1
        )

        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "employee2@gmail.com",
                "password": "employee123"
            },
            format="json"
        )

        employee2_token = login_response.data["access_token"]

        response = self.client.get(
            f"/api/task/{task.id}/",
            HTTP_AUTHORIZATION=f"Bearer {employee2_token}"
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_admin_can_view_any_task(self):

        employee = User.objects.create(
            email="employee@gmail.com",
            role="EMPLOYEE"
        )

        task = Task.objects.create(
            title="Login API",
            description="Create Login API",
            created_by=self.admin,
            assigned_to=employee
        )

        response = self.client.get(
            f"/api/task/{task.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["title"],
            "Login API"
        )