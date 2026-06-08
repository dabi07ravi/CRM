from rest_framework import serializers
from accounts.models import User


class EmployeeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "role",
            "created_at",
            "updated_at"
        )


