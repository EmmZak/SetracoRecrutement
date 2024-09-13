from django.urls import path
from .views import add_skill, delete_skill, skills_data

urlpatterns = [
    path('add_skill/', add_skill, name='add_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'), 
    path('skills_data/', skills_data, name="skills_data")
]