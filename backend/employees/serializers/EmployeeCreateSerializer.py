
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def validate_email(self, value):

        value = value.lower().strip()


        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value