import secrets
import math

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
from employees.serializers.ChangePasswordSerializer import ChangePasswordSerializer


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


                employee = User(
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
                    "user" :  EmployeeGetSerializer(employee).data,
                    "temp_password" : temp_password
                })
        
            except Exception as e:
                print("eeror",e)
                raise


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {
                    "message": "Old password is incorrect"
                },
                status=400
            )

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.must_change_password = False

        user.save()

        return Response(
            {
                "message": "Password changed successfully"
            }
        )



class EmployeeListView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        employees = User.objects.filter(
            role=UserRole.EMPLOYEE
        )

        # Search
        search = request.query_params.get(
            "search"
        )

        if search:
            employees = employees.filter(
                email__icontains=search
            )

        # Sorting
        ordering = request.query_params.get(
            "ordering"
        )

        if ordering:
            employees = employees.order_by(
                ordering
            )

        # Pagination
        page = int(
            request.query_params.get(
                "page",
                1
            )
        )

        page_size = int(
            request.query_params.get(
                "page_size",
                10
            )
        )

        total_count = employees.count()

        start = (page - 1) * page_size

        end = start + page_size

        total_pages = math.ceil(
        total_count / page_size
        )

        employees = employees[start:end]

        serializer = EmployeeGetSerializer(
            employees,
            many=True
        )

        return Response({
            "count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "results": serializer.data
        })
    


class EmployeeDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        employee = get_object_or_404(
            User,
            id=id,
            role=UserRole.EMPLOYEE
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
    

class EmployeeDeleteView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]


    def delete(self, request, id):

        employee = get_object_or_404(
            User,
            id=id,
            role=UserRole.EMPLOYEE
        )

        employee.delete()

        return Response({
            "message": "Employee deleted successfully"
        })
    




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