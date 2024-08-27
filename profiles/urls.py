from django.urls import path
from .views import add_skill, delete_skill
from .views import profiles_view, users_view, home, test, config

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('config/', config, name='config'),  # Placeholder, replace with actual view later
    path('test/', test, name='test'),
    # path('users/', home, name='users'),    # Placeholder, replace with actual view later,
    path('users/', users_view, name='users'),

    # skill
    path('add_skill/', add_skill, name='add_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'), 
]
