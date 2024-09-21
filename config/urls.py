from django.urls import path

from .views import (config_view, create_skill, create_state, delete_skill,
                    delete_state)
from .views_ajax import skills_data, states_data

urlpatterns = [
    path('config/', config_view, name='config'),

    path('create_skill/', create_skill, name='create_skill'),
    #path('delete_skill/<int:pk>/', delete_skill, name='delete_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'),

    path('create_state/', create_state, name='create_state'),
    #path('delete_state/<int:pk>/', delete_state, name='delete_state'),
    path('delete_state/', delete_state, name='delete_state'),

    # ajax
    path('skills_data/', skills_data, name="skills_data"),
    path('states_data/', states_data, name="states_data")
]
