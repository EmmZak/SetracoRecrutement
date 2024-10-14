from django.urls import path

from .views import (config_view, create_skill, create_state, delete_skill,
                    delete_state, create_training, delete_training)
from .views_ajax import skills_data, states_data, trainings_data

urlpatterns = [
    path('config/', config_view, name='config'),

    path('create_skill/', create_skill, name='create_skill'),
    path('delete_skill/', delete_skill, name='delete_skill'),

    path('create_state/', create_state, name='create_state'),
    path('delete_state/', delete_state, name='delete_state'),

    path('create_training/', create_training, name='create_training'),
    path('delete_training/', delete_training, name='delete_training'),

    # ajax
    path('skills_data/', skills_data, name="skills_data"),
    path('states_data/', states_data, name="states_data"),
    path('trainings_data/', trainings_data, name="trainings_data"),
]
