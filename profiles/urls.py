from django.urls import path
from .views import profiles_view, profiles_data, users_view, home, test, config

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('profiles/data', profiles_data, name='profiles_data'),

    path('config/', config, name='config'),  # Placeholder, replace with actual view later
    #path('test/', test, name='test'),
    # path('users/', home, name='users'),    # Placeholder, replace with actual view later,
    path('users/', users_view, name='users'),
]
