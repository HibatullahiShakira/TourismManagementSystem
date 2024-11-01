from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .services import AuthenticationService
import json


auth_service = AuthenticationService()

@api_view()
def home(request):
    #product = Product.objects.get(pk=pk)
    #serializer = ProductSerializer(product)
    #return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'Welcome to the homepage'})

    #LIST
    #products = Product.objects.all()
    #serializer = ProductSerializer(products, many=True)


@csrf_exempt
@require_http_methods(['POST'])
def register_user(request):
    data = json.loads(request.body)
    try:
        user = auth_service.register(data)
        return JsonResponse({
            'id': user.id,
            'message': f'Welcome {user.username}, your account has been successfully created'},
            status=201)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def login_user(request):
    data = json.loads(request.body)
    try:
        response = auth_service.login(data, request)
        return JsonResponse({
            'id': response['id'],
            'message': response['message']
        }, status=response['status_code'])
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurs'})


@csrf_exempt
@require_http_methods(['POST'])
def logout_user(request):
    try:
        response = auth_service.logout(request)
        return JsonResponse({
            'message': response['message']}, status=response['status_code'])
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['PATCH'])
def update_user_profile(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        user_update_data = {
            'username': data.get('username'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'password': data.get('password'),
            'age': data.get('age'),
            'gender': data.get('gender'),
            'is_staff': data.get('is_staff'),
            'phone_number': data.get('phone_number')
        }
        update_user_response = auth_service.update_user_profile(user_id, user_update_data)
        print("Service response:", update_user_response)
        return JsonResponse(update_user_response, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error has occurred'}, status=500)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_user_account(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        user_response = auth_service.delete_account(user_id)
        return JsonResponse(user_response, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error', 'An error occurred'})


@csrf_exempt
@require_http_methods(['GET'])
def get_all_user(request):
    try:
        result = auth_service.get_all_users(request.user.id)
        if 'error' in result:
            return JsonResponse({'error': result['error']}, status=int(result['status_code']))
        return JsonResponse(result, safe=False, status=200)
    except Exception as e:
        print("Error in view:", str(e))
        return JsonResponse({'error': 'Error fetching users'}, status=400)


@csrf_exempt
@require_http_methods
def get_user_by_id(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        user_response = auth_service.delete_account(user_id)
        return JsonResponse(user_response, status=200)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An Error occurred getting user'})
