from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from tasks.models import Task

from accounts.permissions import IsAdmin
from accounts.choices import UserRole
from tasks.choices import TaskStatus


class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        total_employees = User.objects.filter(
            role=UserRole.EMPLOYEE
        ).count()

        total_tasks = Task.objects.count()

        pending_tasks = Task.objects.filter(
            status=TaskStatus.PENDING
        ).count()

        in_progress_tasks = Task.objects.filter(
            status=TaskStatus.IN_PROGRESS
        ).count()

        completed_tasks = Task.objects.filter(
            status=TaskStatus.COMPLETED
        ).count()

        return Response({
            "total_employees": total_employees,
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks
        })