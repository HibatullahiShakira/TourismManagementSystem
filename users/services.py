import re
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse

from .interfaces import AuthenticationServiceInterface

User = get_user_model()


class AuthenticationService(AuthenticationServiceInterface):
    def validate_email(self, email):
        if not email:
            raise ValueError("Email is required")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{3,}$'
        if not re.match(email_regex, email):
            raise ValueError("Enter a valid email address")

    def register(self, user_data):
        self.validate_email(user_data.get('email'))
        required_fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name', 'gender',
                           'phone_number', 'age']
        missing_fields = [field for field in required_fields if field not in user_data or not user_data[field]]

        if missing_fields:
            raise ValueError(f'Missing fields: {', '.join(missing_fields)}')
        password = user_data['password']
        confirm_password = user_data['confirm_password']
        if password != confirm_password:
            raise ValueError("Password does not match")

        if User.objects.filter(username=user_data['username']).exists():
            raise ValueError("A user with that username already exists")

        if User.objects.filter(username=user_data['email']).exists():
            raise ValueError("A user with that email already exists")

        try:
            user = User.objects.create_user(
                username=user_data['username'],
                password=password,
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.gender = user_data['gender']
            user.phone_number = user_data['phone_number']
            user.age = user_data['age']
            user.save()
            return user
        except Exception as e:
            print("Error in user creation:", str(e))
            raise ValueError("User registration failed")

    def login(self, login_data, request):
        username = login_data.get('username')
        password = login_data.get('password')

        if not username or not password:
            raise ValueError("Username and password required")
        user = authenticate(username=login_data['username'], password=login_data['password'])
        if user is not None:
            auth_login(request, user)
            return {
                'id': user.id,
                'message': f'Welcome back, {username}!',
                'status_code': 200
            }
        else:
            raise ValueError("Invalid username or password")

    def logout(self, request):
        auth_logout(request)
        return {
            'message': 'You have been logged out',
            'status_code': 200
        }

    def update_user_profile(self, user_id, user_update_data):
        try:
            user = User.objects.get(id=user_id)
            for field, value in user_update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            user.save()
            return {
                'id': user_id,
                'message': 'Account updated successfully',
                'status_code': 200,
            }
        except User.DoesNotExist:
            raise ValueError('User Account does not exist')
        except Exception as e:
            raise ValueError('Updating account profile Failed')

    def delete_account(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return {'message': 'Account deleted successfully'}
        except User.DoesNotExist:
            raise ValueError('User Account does not exist')
        except Exception as e:
            raise ValueError('Deleting the Account Failed')

    def get_all_users(self, user_id):
        try:
            user_admin = User.objects.get(id=user_id)
            if user_admin.is_staff:
                users = User.objects.all()
                user_list = []
                for user in users:
                    user_list.append({
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password,
                        'date_joined': user.date_joined,
                        'last_login': user.last_login,
                        'age': user.age,
                        'gender': user.gender,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                        'phone_number': user.phone_number,
                    })
                    return user_list
            else:
                return {'error': 'User is not a admin', 'status_code': 403}
        except User.DoesNotExist:
            return {'error': "User account does not exist", 'status_code': 404}
        except Exception as e:
            print("Error in get_all_users:", str(e))
            return {'error': "User account does not exist", 'status_code': 400}

    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.lastname,
                'email': user.email,
                'password': user.password,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'age': user.age,
                'gender': user.gender,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'phone_number': user.phone_number,
            })
        except User.DoesNotExist:
            raise ValueError("User does not exist")
        except Exception as e:
            raise ValueError("Error fetching user details")

