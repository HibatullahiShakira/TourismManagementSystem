import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class UserTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.register_url = reverse('register_user')
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.update_profile_url = reverse('update_user_profile')
        self.delete_user_account_url = reverse('delete_user_account')
        self.get_user_by_id_url = reverse('get_user_by_id')
        self.get_all_user_url = reverse('get_all_user')
        self.user_data = {
            'username': 'Okikiola',
            'password': 'password',
            'confirm_password': 'password',
            'first_name': 'shakirah',
            'last_name': 'Hibatullahi',
            'phone_number': '123456789',
            'age': '23',
            'gender': 'Female',
            'email': 'HibatullahiShakirah@gmail.com',
            'is_staff': False,
        }
        self.admin_user_data = {
            'username': 'admin',
            'password': 'adminpassword',
            'confirm_password': 'adminpassword',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone_number': '987654321',
            'is_staff': True,
            'email': 'HibatullahiShakirah@gmail.com',
            'age': 30,
            'gender': 'Male',
        }

        self.admin_user = User.objects.create_user(
            username=self.admin_user_data['username'],
            password=self.admin_user_data['password'],
            email=self.admin_user_data['email'],
            first_name=self.admin_user_data['first_name'],
            last_name=self.admin_user_data['last_name'],
            age=self.admin_user_data['age'],
            gender=self.admin_user_data['gender'],
            is_staff=self.admin_user_data['is_staff'],
            phone_number=self.admin_user_data['phone_number']
        )

    def test_user_registration(self):
        response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        print(response.content, response.status_code)
        self.assertEqual(response.status_code, 201)
        users_count = User.objects.count()
        print(users_count)
        self.assertEqual(users_count, 2)

    def test_that_successful_registration_return_the_right_message(self):
        response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        print(response.content, response.status_code)
        self.assertEqual(response.json()['message'], 'Welcome Okikiola, your account has been successfully created')

    def test_that_incomplete_user_data_for_register(self):
        incomplete_data = {
            'username': 'Okikiola',
            'password': 'password',
            'confirm_password': 'password',
            'first_name': 'shakirah',
            'last_name': 'Hibatullahi',
            'phone_number': '123456789',
            'age': '23',
            'gender': 'Female'
        }
        response = self.client.post(self.register_url, data=json.dumps(incomplete_data),
                                    content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Email is required')

    def test_user_login(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        login_data = {
            'username': 'Okikiola',
            'password': 'password'
        }
        response = self.client.post(self.login_url, data=login_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_that_user_login_return_the_right_message(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        login_data = {
            'username': 'Okikiola',
            'password': 'password'
        }
        response = self.client.post(self.login_url, data=login_data, content_type='application/json')
        self.assertEqual(response.json()['message'], f'Welcome back, {self.user_data["username"]}!')

    def test_incorrect_password_username(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        login_data = {
            'username': 'Okikiola',
            'password': 'passwords'
        }
        response = self.client.post(self.login_url, data=login_data, content_type='application/json')
        self.assertEqual(response.json().get('error'), "Invalid username or password")

    def test_duplicate_username_registration(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'A user with that username already exists')

    def test_invalid_email_format(self):
        self.user_data['email'] = 'invalidemail'
        response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Enter a valid email address')

    def test_empty_fields(self):
        self.user_data['username'] = ''
        response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Missing fields: username')

    def test_user_logout(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        response = self.client.post(self.logout_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'You have been logged out')

    def test_get_all__users_as_admin(self):
        self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        logged_in = self.client.login(username=self.admin_user_data['username'], password=self.admin_user_data['password'])
        self.assertTrue(logged_in)
        response = self.client.get(self.get_all_user_url, content_type='application/json')
        users = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)

    def test_get_all_users_as_non_admin(self):
        response_users = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        print(response_users.content)
        logged_in = self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        print(logged_in)
        self.assertTrue(logged_in)
        response_users = self.client.get(self.get_all_user_url, content_type='application/json')
        print(response_users.content)
        self.assertEqual(response_users.json()['error'], 'User is not a admin')
        self.assertEqual(response_users.status_code, 403)

    def test_update_user_profile(self):
        create_user_response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        user_id = create_user_response.json()['id']
        update_data = {
            'id': user_id,
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789',
        }
        response = self.client.patch(self.update_profile_url, data=json.dumps(update_data), content_type='application'
                                                                                                         '/json')
        print(response.json())
        self.assertEqual(response.json()['message'], 'Account updated successfully')

    def test_delete_account(self):
        create_user_response = self.client.post(self.register_url, data=self.user_data, content_type='application/json')
        user_id = create_user_response.json()['id']
        data = json.dumps(({'id': user_id}))
        response = self.client.delete(self.delete_user_account_url, data=data, content_type='application/json')
        self.assertEqual(response.json()['message'], 'Account deleted successfully')

