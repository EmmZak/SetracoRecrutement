from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.core.serializers import serialize


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

# @login_required
# @user_passes_test(is_admin)


def groups_data(request):
    groups = list(Group.objects.all().values('id', 'name'))
    print("groups: ", groups)
    response = {
        'groups': groups
    }
    return JsonResponse(response)


def users_data(request):
    users = User.objects.all()

    user_data = [{
        'id': user.id,
        'username': user.username,
        'date_joined': user.date_joined.strftime('%d/%m/%Y'),
        'groups': [{
            'id': group.id,
            'name': group.name
        } for group in user.groups.all()]
    } for user in users]

    response = {
        'users': user_data
    }
    return JsonResponse(response)
