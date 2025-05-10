from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError


class CustomException(ValidationError):
    default_message = _("Invalid")
    status_code = status.HTTP_400_BAD_REQUEST
    error_code_default = 400000

    def __init__(self, message=None, detail=None, code=None, status_code=None, error_code: int = None):
        if status_code is not None:
            self.status_code = status_code

        if message is None:
            message = self.default_message

        if error_code is None:
            error_code = self.error_code_default

        self.message = message
        self.error_code = error_code

        # Ensure detail is a single string (field name)
        if isinstance(detail, dict):
            self.info = detail
        else:
            self.info = {detail: message}

        super().__init__(self.info, code)

    def get(self):
        errors = []
        for field, message in self.info.items():
            errors.append({
                "message": message,
                "field_name": field,
            })

        return {
            "error": errors,
            "error_code": self.status_code,
        }

    def __str__(self):
        return str(self.get())
