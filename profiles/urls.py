from django.urls import path

from .views import (config, home, profile_delete, profiles_create,
                    profiles_create_form, profiles_view)
from .views_ajax import (check_profile, delete_comment, delete_file,
                         export_profile_pdf, export_profiles_csv,
                         profiles_data)

urlpatterns = [
     path('', home, name='home'),
     path('profiles/', profiles_view, name='profiles'),
     path('profile_delete', profile_delete, name='profile_delete'),
     path('profiles_create', profiles_create, name="profiles_create"),
     path('profiles_create_form', profiles_create_form, name="profiles_create_form"),

     # ajax
     path('profiles_data', profiles_data, name='profiles_data'),
     path('check_profile/', check_profile, name='check_profile'),
     path('export_profiles_csv/', export_profiles_csv,
          name='export_profiles_csv'),
     path('export_profile_pdf/',
          export_profile_pdf, name='export_profile_pdf'),
     path('delete_comment/', delete_comment, name="delete_comment"),
     path('delete_file/', delete_file, name='delete_file')
]
