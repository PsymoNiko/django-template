from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled, ValidationError
from .exceptions import CustomException
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If an exception is raised that we want to handle, we can
    # modify the response here.
    if isinstance(exc, AuthenticationFailed):
        custom_response = {
            "error_code": 401,
            "message": "شما اجازه دسترسی به این بخش را ندارید. لطفا وارد شوید.",
            "status": "unauthorized"
        }
        return CustomException(custom_response, status_code=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        custom_response = {
            "error_code": 403,
            "message": "شما اجازه دسترسی به این بخش را ندارید.",
            "status": "forbidden"
        }
        return CustomException(custom_response, status_code=status.HTTP_403_FORBIDDEN)
    if isinstance(exc, CustomException):
        response.data = exc.get()
    elif isinstance(exc, ValidationError):
        detail = exc.detail
        formatted_errors = []
        for field, errors in detail.items():
            for error in errors:
                formatted_errors.append({
                    "message": error,
                    "field_name": field
                })

        response.data = {
            "error": formatted_errors,
            "error_code": response.status_code,
        }
    elif isinstance(exc, Throttled):
        response.data = {
            "error": [
                {
                    "message": "Too many attempts. Please wait 5 minutes.",
                    "field_name": "phone_number"
                }
            ],
            "error_code": response.status_code,
        }
    return response
