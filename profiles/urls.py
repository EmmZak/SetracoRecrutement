from django.urls import path
from .views import profile_delete, profiles_view, profiles_create, home, config
from .views_ajax import profiles_data, check_profile, export_profiles_csv, delete_comment

urlpatterns = [
    path('', home, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('profile_delete', profile_delete, name='profile_delete'),
    path('profiles_create', profiles_create, name="profiles_create"),

    # ajax
    path('profiles_data', profiles_data, name='profiles_data'),
    path('check_profile/', check_profile, name='check_profile'),
    path('export_profiles_csv/', export_profiles_csv,
         name='export_profiles_csv'),
    path('delete_comment/', delete_comment, name="delete_comment"),


    # Placeholder, replace with actual view later
    path('config/', config, name='config'),
    # path('test/', test, name='test'),
    # path('users/', home, name='users'),    # Placeholder, replace with actual view later,
    # path('users/', users_view, name='users'),
]
