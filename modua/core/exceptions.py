from rest_framework.exceptions import APIException

class Raise403(APIException):
    status_code = 403
    default_detail = 'Request Forbidden.'
