from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TourTest(TestCase):
    client = Client()

    def setUp(self):
        self.create_tour_url = reverse('create_tour')
        self.update_tour_url = reverse('update_tour')
        self.delete_tour_url = reverse('delete_tour')
        self.get_tour_by_name_url = reverse('get_tour_by_name')
        self.get_tour_by_location_url = reverse('get_tour_by_location')
        self.get_all_tours = reverse('get_all_tours')
        self.get_tour_by_id = reverse('get_tour_by_id')

        self.tour_data = {
            'name': 'safari',
            'availability': 'True',
            'description': 'Exciting safari tour',
            'price': 1000,
            'location': 'Kenya'
        }
        User = get_user_model()
        self.admin_user_data = {
            'username': 'shakira',
            'password': 'shakirapassword',
            'confirm_password': 'shakirapassword',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone_number': '987654321',
            'is_staff': True,
            'email': 'Hibatullahi@gmail.com',
            'age': 30,
            'gender': 'Male',
        }
        self.user_data = {
            'username': 'Ashakun',
            'password': 'password',
            'confirm_password': 'password',
            'first_name': 'shakirah',
            'last_name': 'Hibatullahi',
            'phone_number': '123456789',
            'age': '23',
            'gender': 'Female',
            'email': 'Shakirah@gmail.com',
            'is_staff': False,
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            age=self.user_data['age'],
            gender=self.user_data['gender'],
            is_staff=self.user_data['is_staff'],
            phone_number=self.user_data['phone_number']
        )

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

    def test_create_tour_as_admin_successful(self):
        logged_in = self.client.login(username=self.admin_user_data['username'],
                                      password=self.admin_user_data['password'])
        print(logged_in)
        self.assertTrue(logged_in)
        response = self.client.post(self.create_tour_url, data=self.tour_data, content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 201)

    def test_create_tour_as_non_admin_successful(self):
        logged_in = self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        print(logged_in)
        self.assertTrue(logged_in)
        response = self.client.post(self.create_tour_url, data=self.tour_data, content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{"error": "Only staff members can create tour"}')

    def test_create_tour_with_missing_data(self):
        incomplete_data = {
            'name': 'Paris Tower',
            'availability': 'True',
            'description': 'City of ',
            'price': 1000,
        }
        logged_in = self.client.login(username=self.admin_user_data['username'],
                                      password=self.admin_user_data['password'])
        self.assertTrue(logged_in)
        response = self.client.post(self.create_tour_url, data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"error": "Missing Fields: location"}')

    def test_negative_price(self):
        tour_data = {
            'name': 'safari',
            'availability': 'True',
            'description': 'Exciting safari tour',
            'price': -1000,
            'location': 'Kenya'
        }
        logged_in = self.client.login(username=self.admin_user_data['username'],
                                      password=self.admin_user_data['password'])
        print(logged_in)
        self.assertTrue(logged_in)
        response = self.client.post(self.create_tour_url, data=tour_data, content_type='application/json')
        print(response.content)
        self.assertEqual(response.json()['error'], 'Price must not be less than zero')
        self.assertEqual(response.status_code, 400)

    def test_update_tour_as_admin_successful(self):
        logged_in = self.client.login(username=self.admin_user_data['username'],
                                      password=self.admin_user_data['password'])
        self.assertTrue(logged_in)
        print(logged_in)
        user_id = self.admin_user.id
        print(user_id)
        update_data = {
            'id': user_id,
            'name': 'Paris Museum',
            'description': 'Home of collections as arts ',
        }
        response = self.client.patch(self.update_tour_url, data=update_data, content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"error": "Updated tour"}')
