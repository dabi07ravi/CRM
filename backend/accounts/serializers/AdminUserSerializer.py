from rest_framework import serializers
from accounts.models import User



class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "role",
            "must_change_password",
            "created_at",
            "updated_at"
        )