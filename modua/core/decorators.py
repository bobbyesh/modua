from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status


def required_request_data(params):
    assert hasattr(params, '__iter__'), 'required_params only takes an iterable'
    def decorator(func):
        def method_wrapper(self, *args, **kwargs):
            for param in params:
                if param not in self.request.data:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': 'query param {} required'.format(param)}
                    )
            return func(self, *args, **kwargs)
        return method_wrapper
    return decorator
