import secrets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.choices import UserRole
from accounts.permissions import IsAdmin

from django.contrib.auth import get_user_model

User = get_user_model()

from employees.serializers.EmployeeCreateSerializer import EmployeeCreateSerializer
from employees.serializers.EmployeeGetSerilaizer import EmployeeGetSerializer


class EmployeeCreateView(APIView):
        
        permission_classes = [IsAuthenticated, IsAdmin]
        def post(self, request):

            try:
                serializer = EmployeeCreateSerializer(
                    data=request.data
                )

                serializer.is_valid(
                    raise_exception=True
                )

                temp_password = secrets.token_urlsafe(8)

                employee = User.objects.create(
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    role=UserRole.EMPLOYEE,
                    must_change_password=True
                )

                employee.set_password(temp_password)
                employee.save()

                serializer = EmployeeGetSerializer(employee)

                return Response({
                    "message": "Employee created successfully",
                    "user" : serializer.data
                })
        
            except Exception as e:
                print("eeror",e)
                raise
