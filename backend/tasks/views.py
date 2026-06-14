from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

from tasks.models import Task
from tasks.serilaizers.TaskCreateSerializer import TaskCreateSerializer
from tasks.serilaizers.TaskListSerializer import TaskListSerializer
from tasks.serilaizers.TaskAssignSerializer import TaskAssignSerializer
from tasks.serilaizers.TaskStatusSerializer import TaskStatusSerializer

from accounts.permissions import IsAdmin, IsEmployee

from accounts.choices import UserRole


class TaskCreateView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        serializer = TaskCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = Task.objects.create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data["description"],
            assigned_to=None,
            created_by=request.user
        )

        return Response(
            {
                "message": "Task created successfully",
                "task_id": task.id
            },
            status=status.HTTP_201_CREATED
        )
    

class TaskListView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        tasks = Task.objects.all().order_by("-created_at")

        serializer = TaskListSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)
    
class MyTaskListView(APIView):

    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):

        tasks = Task.objects.filter(
            assigned_to=request.user
        ).order_by("-created_at")

        serializer = TaskListSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)
    

class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        task = get_object_or_404(
            Task,
            id=id
        )

        if (
            request.user.role == UserRole.EMPLOYEE
            and task.assigned_to != request.user
        ):
            return Response(
                {
                    "message": "Permission denied"
                },
                status=403
            )

        serializer = TaskListSerializer(task)

        return Response(serializer.data)
    

class TaskAssignView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, id):

        serializer = TaskAssignSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = get_object_or_404(
            Task,
            id=id
        )

        employee = get_object_or_404(
            User,
            id=serializer.validated_data["employee_id"]
        )

        if employee.role != UserRole.EMPLOYEE:
            return Response(
                {
                    "message": "Task can only be assigned to an employee"
                },
                status=400
            )

        task.assigned_to = employee

        task.save()

        return Response(
            {
                "message": "Task assigned successfully"
            }
        )
    

class TaskStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, id):

        task = get_object_or_404(
            Task,
            id=id
        )

        if (
            request.user.role == UserRole.EMPLOYEE
            and task.assigned_to != request.user
        ):
            raise PermissionDenied(
                "You cannot update this task."
            )

        serializer = TaskStatusSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        task.status = serializer.validated_data["status"]

        task.save()

        return Response({
            "message": "Task status updated successfully"
        })
    

class TaskDeleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def delete(self, request, id):

        task = get_object_or_404(
            Task,
            id=id
        )

        task.delete()

        return Response({
            "message": "Task deleted successfully"
        })
    
