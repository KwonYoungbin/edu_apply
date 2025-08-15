# utils/responses.py
from rest_framework.response import Response
from rest_framework import status

def success(message=None, data=None, code=status.HTTP_200_OK):
    body = {
        'success': True,
    }
    if message is not None:
        body['message'] = message
    if data is not None:
        body["data"] = data
    return Response(body, status=code)


def error(message=None, code=status.HTTP_400_BAD_REQUEST, errors=None):
    body = {
        'success': False,
    }
    if message is not None:
        body['message'] = message
    if errors is not None:
        body["errors"] = errors
    return Response(body, status=code)
