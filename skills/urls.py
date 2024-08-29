from django.urls import path
from .views import add_skill, delete_skill, skill_list

urlpatterns = [
    path('add_skill/', add_skill, name='add_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'), 
    path('skills/', skill_list, name="skill_list")
]