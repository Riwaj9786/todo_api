from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todo_app import models

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
        
        # Extract the access and refresh token
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Log out using the refresh token
        logout_data = {
            "refresh_token": refresh_token
        }
        response = self.client.post(reverse('account_logout'), logout_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="example",
            password="NewPassword@123",
            is_active = True
        )

        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        login_response = self.client.post(reverse('token_obtain_pair'), data)
        print(login_response.data)

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        self.todolist = models.TodoList.objects.create(
            title="Test Case Init",
            description="Suppose I have described about the initial test case.",
            status="To Do"
        )

    
    def test_todolist_create(self):
        data = {
            "title": "Test Case",
            "description": "Suppose I have described about the test case.",
            "status": "To Do"
        }
        response = self.client.post(reverse('todo_app:todo-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_todolist_list(self):
        response = self.client.get(reverse('todo_app:todo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)