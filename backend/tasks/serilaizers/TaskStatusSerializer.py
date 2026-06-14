from rest_framework import serializers

from tasks.choices import TaskStatus


class TaskStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=TaskStatus.choices
    )