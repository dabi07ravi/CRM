from rest_framework import serializers


class TaskAssignSerializer(serializers.Serializer):

    employee_id = serializers.IntegerField()