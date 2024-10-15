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