from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/', views.user_list, name='users'),

    path('users_data', views.users_data, name='users_data'),
    path('groups_data/', views.groups_data, name="groups_data"),


    path('users_create/', views.users_create, name='users_create'),
    path('users_delete', views.users_delete, name="users_delete"),

    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    # path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    #path('delete_user/', views.delete_user, name='delete_user'),

    #
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
