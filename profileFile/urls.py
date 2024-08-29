from django.urls import path
from .views import delete_file

urlpatterns = [
    path('delete-file/', delete_file, name='delete_file'),
]
