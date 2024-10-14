from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from SetracoRecrutement.logger import Logger
from .services import find_all_states, find_all_skills

logger = Logger('config')

@login_required
def skills_data(request):
    logger.debug("fetching skills data")
    skills = find_all_skills()
    skills_list = list(skills)
    return JsonResponse(skills_list, safe=False)

@login_required
def states_data(request):
    logger.debug("fetching states data")
    states = find_all_states()
    states_list = list(states)
    return JsonResponse(states_list, safe=False)
