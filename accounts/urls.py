from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/', views.user_list, name='users'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    # path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('delete_user/', views.delete_user, name='delete_user'),

    #
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
