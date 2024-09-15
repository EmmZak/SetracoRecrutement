from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from profileFile.models import ProfileFile
from skills.models import Skill
from .models import Profile, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import ProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from django.core.serializers import serialize
import csv
from django.http import HttpResponse


def config(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        return render(request, 'config.html', {'skills': skills})


def profiles_view(request):
    is_superuser = request.user.is_superuser

    is_editor_or_admin = request.user.groups.filter(
        name__in=['Editeur', 'Admin']).exists()
    
    is_editor_or_admin_or_superuser = is_superuser or is_editor_or_admin
    print("is_editor_or_admin: ", is_editor_or_admin_or_superuser)

    return render(request, 'profiles.html', {'is_editor_or_admin': is_editor_or_admin_or_superuser})


@login_required
@require_http_methods(["POST"])
def profiles_create(request):

    profile_id = request.POST.get('id')
    surname = request.POST.get('surname')
    name = request.POST.get('name')
    town = request.POST.get('town')
    email = request.POST.get('email')
    number = request.POST.get('number')
    # skills = request.POST.get('skills')
    # skills = request.POST.getlist('skills')
    # selected_skill_ids = request.POST.getlist('skills')
    diplomas = request.POST.get('diplomas')
    comment = request.POST.get('comment')
    state = request.POST.get('state', None)
    print("state:  ", state)
    if state == None or state == "":
        state = Profile.STATE_TO_VERIFY

    # print(surname, name, town, email, number,"skills: ", skills, diplomas, comment, state)
    # profile = None
    new_profile = None
    if profile_id:
        Profile.objects.filter(id=profile_id).update(
            surname=surname,
            name=name,
            town=town,
            email=email,
            number=number,
            diplomas=diplomas,
            # comment=comment,
            state=state
        )
    else:
        new_profile = Profile.objects.create(
            surname=surname,
            name=name,
            town=town,
            email=email,
            number=number,
            diplomas=diplomas,
            # comment=comment,
            state=state
        )

    if profile_id:
        profile = Profile.objects.filter(id=profile_id).first()
    else:
        profile = new_profile

    # comment
    if comment:
        Comment.objects.create(
            profile=profile,
            user=request.user,
            text=comment
        )

    skill_ids = request.POST.get('skills', '')

    if skill_ids:
        selected_skill_ids = list(map(int, skill_ids.split(',')))
        selected_skills = Skill.objects.filter(id__in=selected_skill_ids)
        profile.skills.set(selected_skills)
    else:
        profile.skills.clear()

    # Handle file uploads
    # print("request.FILES: ", request.FILES)
    if 'files' in request.FILES:
        uploaded_files = request.FILES.getlist('files')
        # print("uploaded_files: ", uploaded_files)
        for file in uploaded_files:
            print("file: ", file, type(file))
            document = ProfileFile.objects.create(profile=profile, file=file)
            profile.files.add(document)

    return redirect('/profiles')


@require_http_methods(["DELETE"])
def profile_delete(request):
    profile_id = request.GET.get('id')
    if profile_id:
        Profile.objects.filter(id=profile_id).delete()
    return redirect('/profiles')


@login_required
def home(request):
    return render(request, 'home.html')
