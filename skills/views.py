from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from skills.models import Skill

def skill_list(request):
    skills = Skill.objects.all().values('id', 'name')
    skills_list = list(skills)
    return JsonResponse(skills_list, safe=False)

# Create your views here.
def add_skill(request):
    if request.method == 'POST':
        # Add a new skill
        skill_name = request.POST.get('skill_name')
        if skill_name:
            Skill.objects.create(name=skill_name)
        return redirect('/config')

@require_http_methods(["POST"])
def delete_skill(request):
    skill_id = request.POST.get('id')
    if skill_id:
        Skill.objects.filter(id=skill_id).delete()

    return redirect('/config')