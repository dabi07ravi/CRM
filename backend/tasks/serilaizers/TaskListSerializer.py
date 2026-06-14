from rest_framework import serializers

from tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "assigned_to",
            "created_at",
            "updated_at"
        )