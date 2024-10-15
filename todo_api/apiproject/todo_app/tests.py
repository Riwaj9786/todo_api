from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password1": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        response = self.client.post(reverse('account_signup'), data)

        self.assertRedirects(response, expected_url=reverse('account_email_verification_sent'))
        self.assertTrue(User.objects.filter(username="testcase").exists())


class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example",
                                            password="NewPassword@123")
                                         
    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.access_token = response.data['access']


    def test_logout(self):
        # Perform login to get the token
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        login_response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # Extract the access token
        access_token = login_response.data['access']
        
        # Add Authorization header with JWT token for logout request
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Assuming there's a logout endpoint defined (e.g., at 'account_logout')
        response = self.client.post(reverse('account_logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

