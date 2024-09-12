from django.urls import path
from .views import profile_delete, profiles_view, profiles_data, profiles_create, home, config

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('profiles_data', profiles_data, name='profiles_data'),
    path('profile_delete', profile_delete, name='profile_delete'),
    path('profiles_create', profiles_create, name="profiles_create"),

    # Placeholder, replace with actual view later
    path('config/', config, name='config'),
    # path('test/', test, name='test'),
    # path('users/', home, name='users'),    # Placeholder, replace with actual view later,
    # path('users/', users_view, name='users'),
]
