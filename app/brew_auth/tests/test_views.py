import json
from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase


class BrewAuthApiUnittest(APITestCase):
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

    @mock.patch("brew_auth.views.UserCreateSerializer", autospec=True)
    @mock.patch("brew_auth.views.api_settings.JWT_PAYLOAD_HANDLER",
                autospec=True)
    @mock.patch("brew_auth.views.api_settings.JWT_ENCODE_HANDLER",
                autospec=True)
    def test_user_registration_ok(
            self,
            mock_jwtencode_handler,
            mock_jwtpayload_handler,
            mock_serializer
    ):
        """It should be possible for user to register and obtain JWT auth token."""
        mock_jwt_encode_return = mock.Mock().return_value = '1234'
        mock_jwtencode_handler.return_value = mock_jwt_encode_return
        mock_jwtpayload_handler.return_value = None
        save_mock_ret_val = 'mock_save_return_value'
        mock_serializer.return_value.save.return_value = save_mock_ret_val
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data=self.user_reg,
                                    format='json'
                                    )
        mock_jwtpayload_handler.assert_called_once_with(save_mock_ret_val)
        mock_jwtencode_handler.assert_called_once_with(None)
        mock_serializer.assert_called_once_with(data=self.user_reg)
        mock_serializer.return_value.is_valid.assert_called_once()
        mock_serializer.return_value.save.assert_called_once_with()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(mock_jwt_encode_return, json.loads(response.content))

    @mock.patch("brew_auth.views.UserCreateSerializer", autospec=True)
    def test_user_registration_user_data_validation_fail(
            self,
            mock_serializer
    ):
        """Bad request should be returned if user data validation fails"""
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = 'serializer error'
        response = self.client.post(f'{self.BASE_AUTH_APP_URL}/register/',
                                    data=self.user_reg,
                                    format='json'
                                    )
        mock_serializer.return_value.is_valid.assert_called_once_with()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(mock_serializer.return_value.errors,
                         json.loads(response.content))
