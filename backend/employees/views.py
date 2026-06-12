import secrets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.choices import UserRole
from accounts.permissions import IsAdmin

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


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

                print("temppp", temp_password)

                employee = User.objects.create(
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    role=UserRole.EMPLOYEE,
                    must_change_password=True
                )

                employee.set_password(temp_password)
                employee.save()

                return Response({
                    "message": "Employee created successfully",
                    "user" :  EmployeeGetSerializer(employee).data
                })
        
            except Exception as e:
                print("eeror",e)
                raise



class EmployeeListView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        employees = User.objects.filter(role=UserRole.EMPLOYEE)

        serializer = EmployeeGetSerializer(
            employees,
            many=True
        )

        return Response(serializer.data)
    


class EmployeeDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        employee = get_object_or_404(
            User,
            id=id,
            role="EMPLOYEE"
        )

        if (
            request.user.role == "EMPLOYEE"
            and request.user.id != employee.id
        ):
            return Response(
                {"message": "Permission denied"},
                status=403
            )

        serializer = EmployeeGetSerializer(employee)

        return Response(serializer.data)
    




class UploadProfilePictureView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        user = request.user

        user.profile_pic = request.FILES.get(
            "profile_pic"
        )

        user.save()

        return Response({
            "message": "Profile picture uploaded"
        })