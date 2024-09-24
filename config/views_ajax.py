from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from SetracoRecrutement.logger import Logger

from .models import Skill, State

logger = Logger('config')

@login_required
def skills_data(request):
    logger.debug("fetching skills data")
    skills = Skill.objects.all().values('id', 'name')
    skills_list = list(skills)
    return JsonResponse(skills_list, safe=False)

@login_required
def states_data(request):
    logger.debug("fetching states data")
    states = State.objects.all().values('id', 'name')
    states_list = list(states)
    return JsonResponse(states_list, safe=False)
