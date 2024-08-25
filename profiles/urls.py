from django.urls import path
from .views import profiles_view, users_view, home, test

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('config/', home, name='config'),  # Placeholder, replace with actual view later
    path('test/', test, name='test'),
    # path('users/', home, name='users'),    # Placeholder, replace with actual view later,
    path('users/', users_view, name='users'),
]
