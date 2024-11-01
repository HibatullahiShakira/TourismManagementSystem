from django.urls import path
from .views import (register_user, logout_user, login_user, home, update_user_profile, delete_user_account,
                    get_user_by_id, get_all_user)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('update/profile/', update_user_profile, name='update_user_profile'),
    path('delete_user/', delete_user_account, name='delete_user_account'),
    path('get_user/', get_user_by_id, name='get_user_by_id'),
    path('users/', get_all_user, name='get_all_user')
]
