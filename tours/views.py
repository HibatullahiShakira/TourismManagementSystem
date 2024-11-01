import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TourSerializer

from .services import TourService

tour_service = TourService()


def home(request):
    return JsonResponse({'message': 'Welcome to the Tour page'})


@api_view(['POST'])
def create_tour(request):
    user = request.user
    try:
        tour = tour_service.create_tour(user, request.data)
        serializer = TourSerializer(tour)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except PermissionError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def update_tour(request):
    user = request.user
    tour_id = request.data.get('id')
    try:
        tour = tour_service.update_tour(user, tour_id, request.data)
        serializer = TourSerializer(tour)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PermissionError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_tour(request):
    user = request.body
    try:
        tour_id = request.data.get('id')
        tour_response = tour_service.delete_tour(user, tour_id)
        return Response(tour_response, status=status.HTTP_200_OK)
    except PermissionError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error', 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_tours(request):
    try:
        if not request.user.is_staff:
            return Response({'error': 'User is not an admin'}, status=403)
        tours = tour_service.list_all_tour()
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': 'An error occurred fetching tours'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_tour_by_name(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        tours = tour_service.get_tour_by_name(name)
        serializers = TourSerializer(tours, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': 'Error occurred fetching tours'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_tour_by_location(request):
    try:
        data = json.loads(request.body)
        location = data.get('location')
        tours = tour_service.get_tour_by_location(location)
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return JsonResponse({'error': 'Error occurred fetching tours'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_tour_by_id(request):
    try:
        data = json.loads(request.body)
        tour_id = data('id')
        tour = tour_service.get_tour_by_id(tour_id)
        serializer = TourSerializer(tour)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': 'Error occurred getting tour'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
