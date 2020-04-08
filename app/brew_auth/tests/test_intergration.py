import json
import unittest
from unittest import mock
from unittest.mock import call

import requests
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.utils import jwt_decode_handler

User = get_user_model()


class BrewAuthApiIntegrationTest(APITestCase):
    """Test complete integration between views, serailizers and models"""
    BASE_AUTH_APP_URL = '/api/v0/brew_auth'

    def setUp(self):
        self.user_reg = {
            'username': 'test_name',
            'email': 'test@test.com',
            'password': 'test_password',
            'password2': 'test_password'
        }

        self.user_log = {
            'username': 'test_name',
            'password': 'test_password',
        }

    def test_user_registration_provides_jwt_token(self):
        """It should be possible for user to register and obtain JWT auth token.
        
        """
        users = User.objects.all()
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data=self.user_reg,
                                    format='json'
                                    )
        jwt_response = response.data
        # Should not raise if token is valid
        decode_jwt = jwt_decode_handler(jwt_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration_fail(self):
        """It should not be possible for user to register with faulty request data
        
        """
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data={},
                                    format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_provides_jwt_token(self):
        """It should be possible for logged in user to obtain JWT auth token.
        
        """
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data=self.user_reg,
                                    format='json'
                                    )
        # Ensure user is registered
        jwt_response = response.data
        # Should not raise if token is valid
        decode_jwt = jwt_decode_handler(jwt_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/login/',
                                    data=self.user_log,
                                    format='json'
                                    )
        jwt_response = response.data
        # Should not raise if token is valid
        decode_jwt = jwt_decode_handler(jwt_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_user(self):
        """It should not be possible for user to login if not registered first!
        
        """
        expected_response_message = 'Not found.'
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/login/',
                                    data=self.user_log,
                                    format='json'
                                    )
        self.assertEqual(expected_response_message,
                         json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_jwt_token(self):
        """Ensure HTTP_200_OK is returned when verifying valid jwt token."""
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data=self.user_reg,
                                    format='json'
                                    )
        jwt_response = response.data
        # Should not raise if token is valid
        decode_jwt = jwt_decode_handler(jwt_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request_data = {'token': jwt_response}
        response = self.client.post(f'/api-token-verify/',
                                    data=request_data,
                                    format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_jwt_token_fail(self):
        """Ensure HTTP_400_BAD_REQUEST is returned when verifying invalid jwt token."""
        expected_response_data = {
            'non_field_errors': ['Error decoding signature.']}
        request_data = {'token': '112355'}
        response = self.client.post(f'/api-token-verify/',
                                    data=request_data,
                                    format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected_response_data, json.loads(response.content))
