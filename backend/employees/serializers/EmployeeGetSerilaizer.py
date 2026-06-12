from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "must_change_password",
            "profile_pic",
            "created_at",
        )