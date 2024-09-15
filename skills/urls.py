from django.urls import path
from .views import add_skill, delete_skill
from .views_ajax import skills_data

urlpatterns = [
    path('add_skill/', add_skill, name='add_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'), 
    # ajax
    path('skills_data/', skills_data, name="skills_data")
]