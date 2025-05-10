from rest_framework.response import Response


# class CustomResponse(Response):
#     def __init__(self, data=None, status=None, message=None, success=True, **kwargs):
#
#         standard_response = {
#             'status': status,
#             'data': data,
#         }
#         super().__init__(data=standard_response, status=status, **kwargs)

class CustomResponse(Response):
    def __init__(self, data=None, status=None, message=None, success=True, **kwargs):
        # Check if the data contains pagination keys
        if isinstance(data, dict) and all(key in data for key in ['page', 'per_page', 'page_count', 'total']):
            standard_response = {
                'status': status,
                'data': data.get('data', []),
                'page': data.get('page'),
                'per_page': data.get('per_page'),
                'page_count': data.get('page_count'),
                'total': data.get('total'),
            }
        else:
            standard_response = {
                'status': status,
                'data': data,
            }

        super().__init__(data=standard_response, status=status, **kwargs)


