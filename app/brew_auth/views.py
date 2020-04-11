from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserCreateSerializer

User = get_user_model()

registration_user_response = openapi.Response(
    'User Auth JWT token', UserCreateSerializer)
registration_swagger_responses = {
    201: registration_user_response, 400: 'Invalid user data'}
login_swagger_responses = {200: 'User Auth JWT token', 404: 'User not found'}


@swagger_auto_schema(methods=['post'], request_body=UserCreateSerializer,
                     responses=registration_swagger_responses)
@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    """End point for user registration and obtaining JWT auth token.

    """
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response(token, status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    responses=login_swagger_responses,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING,
                                       description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING,
                                       description='password'),
        },
    ))
@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    """End point for user login and obtaining new JWT auth token.

    """
    user = get_object_or_404(User, username=request.data['username'])
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response(token, status.HTTP_200_OK)
