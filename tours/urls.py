from django.urls import path
from .views import (create_tour, update_tour, delete_tour, get_tour_by_name, get_tour_by_location, get_all_tours,
                    get_tour_by_id)

urlpatterns = [
    path('add_tour/', create_tour, name='create_tour'),
    path('update/tour/', update_tour, name='update_tour'),
    path('delete/tour/', delete_tour, name='delete_tour'),
    path('get_tour_name/', get_tour_by_name, name='get_tour_by_name'),
    path('get_tour_location/', get_tour_by_location, name='get_tour_by_location'),
    path('tours/', get_all_tours, name='get_all_tours'),
    path('tour_id/', get_tour_by_id, name='get_tour_by_id'),
]
