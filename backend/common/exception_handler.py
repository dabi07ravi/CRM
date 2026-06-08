from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response



def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
        {
            "success": False,
            "message": "Internal server error",
            "errors": {}
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

    message_map = {
        status.HTTP_400_BAD_REQUEST: "Validation failed",
        status.HTTP_401_UNAUTHORIZED: "Authentication failed",
        status.HTTP_403_FORBIDDEN: "Permission denied",
        status.HTTP_404_NOT_FOUND: "Resource not found",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error",
    }


    message = message_map.get(
        response.status_code,
        "Request failed"
    )

    response.data = {
        "success": False,
        "message": message,
        "errors": response.data,
    }

    return response