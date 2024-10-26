from django.urls import path

from .views import (config, profile_delete, profiles_create,
                    profiles_view, error_page)
from .views_ajax import (check_profile, delete_comment, delete_followup, delete_file,
                         export_profile_pdf, export_profiles_csv,
                         profiles_data)

urlpatterns = [
    path('', profiles_view, name='profiles'),
    path('profiles/', profiles_view, name='profiles'),
    path('error/', error_page, name='error_page'),
    path('profile_delete', profile_delete, name='profile_delete'),
    path('profiles_create', profiles_create, name="profiles_create"),


    # ajax
    path('profiles_data', profiles_data, name='profiles_data'),
    path('check_profile/', check_profile, name='check_profile'),
    path('export_profiles_csv/', export_profiles_csv,
         name='export_profiles_csv'),
    path('export_profile_pdf/',
         export_profile_pdf, name='export_profile_pdf'),
    path('delete_comment/', delete_comment, name="delete_comment"),
    path('delete_followup/', delete_followup, name="delete_followup"),
    path('delete_file/', delete_file, name='delete_file')
]
