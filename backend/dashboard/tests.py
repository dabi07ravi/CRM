from rest_framework.test import APITestCase

from accounts.models import User
from tasks.models import Task

from tasks.choices import TaskStatus



class DashboardTestCase(APITestCase):

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


    def test_dashboard_total_employees_count(self):

        User.objects.create(
            email="employee1@gmail.com",
            role="EMPLOYEE"
        )

        User.objects.create(
            email="employee2@gmail.com",
            role="EMPLOYEE"
        )

        response = self.client.get(
            "/api/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["total_employees"],
            2
        )

    def test_dashboard_total_tasks_count(self):

        Task.objects.create(
            title="Task 1",
            description="Demo",
            created_by=self.admin
        )

        Task.objects.create(
            title="Task 2",
            description="Demo",
            created_by=self.admin
        )

        Task.objects.create(
            title="Task 3",
            description="Demo",
            created_by=self.admin
        )

        response = self.client.get(
            "/api/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["total_tasks"],
            3
        )

    def test_dashboard_pending_tasks_count(self):

        Task.objects.create(
            title="Task 1",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.PENDING
        )

        Task.objects.create(
            title="Task 2",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.PENDING
        )

        Task.objects.create(
            title="Task 3",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.COMPLETED
        )

        response = self.client.get(
            "/api/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.data["pending_tasks"],
            2
        )
    def test_dashboard_in_progress_tasks_count(self):

        Task.objects.create(
            title="Task 1",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.IN_PROGRESS
        )

        Task.objects.create(
            title="Task 2",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.IN_PROGRESS
        )

        Task.objects.create(
            title="Task 3",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.PENDING
        )

        response = self.client.get(
            "/api/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.data["in_progress_tasks"],
            2
        )

    def test_dashboard_completed_tasks_count(self):

        Task.objects.create(
            title="Task 1",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.COMPLETED
        )

        Task.objects.create(
            title="Task 2",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.COMPLETED
        )

        Task.objects.create(
            title="Task 3",
            description="Demo",
            created_by=self.admin,
            status=TaskStatus.PENDING
        )

        response = self.client.get(
            "/api/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(
            response.data["completed_tasks"],
            2
        )