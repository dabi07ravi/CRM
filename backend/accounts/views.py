from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed



from accounts.serializers.AdminUserSerializer import AdminUserSerializer

from accounts.serializers.EmployeeUserSerializer import EmployeeUserSerializer

class LoginView(APIView):

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        refresh = RefreshToken.for_user(user)

        refresh["email"] = user.email
        refresh["role"] = user.role


        if user.role.upper() == 'ADMIN':
            serializer = AdminUserSerializer(user)
        else:
            serializer = EmployeeUserSerializer(user)

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user" : serializer.data
        })