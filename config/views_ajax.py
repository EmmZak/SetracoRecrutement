from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from .models import Skill, State

@login_required
def skills_data(request):
    skills = Skill.objects.all().values('id', 'name')
    skills_list = list(skills)
    return JsonResponse(skills_list, safe=False)

@login_required
def states_data(request):
    states = State.objects.all().values('id', 'name')
    states_list = list(states)
    return JsonResponse(states_list, safe=False)
