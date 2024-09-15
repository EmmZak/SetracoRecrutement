from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from profileFile.models import ProfileFile
from profiles.serializers import ProfileSerializer
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
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers


@require_http_methods(["DELETE"])
def delete_comment(request):
    com_id = request.GET.get('id')
    print("deleting comment: ", com_id)
    if com_id:
        Comment.objects.filter(id=com_id).delete()
        print("returning success")
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required
def export_profiles_csv(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search', '')
    # Filter by skills (assuming the skill filter is a comma-separated list of skill IDs)
    skill_filter = request.GET.get('skills', '')
    state_filter = request.GET.get('states', '')

    profiles = Profile.objects.all()
    if search_value:
        profiles = profiles.filter(
            Q(name__icontains=search_value) |
            Q(surname__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(number__icontains=search_value)
        )

    if skill_filter:
        skill_ids = skill_filter.split(',')
        profiles = profiles.filter(skills__id__in=skill_ids).distinct()

    if state_filter:
        states = state_filter.split(',')
        print("states: ", states)
        profiles = profiles.filter(state__in=states)

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'Nom', 'Prénom', 'Email', 'Numéro', 'Ville', 'Compétences', 'Diplômes',
        'Date de création', 'Date de mise à jour', 'État', 'Commentaires'
    ])

    # Write the data rows
    for profile in profiles:
        # Get all skills as a comma-separated string
        skills = ', '.join([skill.name for skill in profile.skills.all()])

        # Get all comments as a combined string
        comments = '; '.join(
            [f"{comment.user.username}: {comment.text}" for comment in profile.comments.all()])

        profile_states = {
            "STATE_TO_VERIFY": "À vérifier",
            "STATE_VERIFIED": "Vérifié",
            "STATE_CONSULTED": "Consulté",
            "STATE_HIRED": "Embauché",
            "STATE_REJECTED": "Rejeté"
        }
        state = profile_states.get(profile.state, 'Inconnu')
        creation_date = profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')
        update_date = profile.update_date.strftime('%d/%m/%Y %H:%M:%S')

        writer.writerow([
            profile.name, profile.surname, profile.email, profile.number, profile.town,
            skills, profile.diplomas, creation_date, update_date, state, comments
        ])

    return response


@login_required
@require_http_methods(["GET"])
def check_profile(request):
    data = request.GET
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    number = data.get('number')

    result = {}
    print("simi check", name, surname, email, number)
    if Profile.objects.filter(name=name).exists():
        # result['name'] = True
        pass
    if Profile.objects.filter(surname=surname).exists():
        # result['surname'] = True
        pass
    if Profile.objects.filter(email=email).exists():
        result['email'] = True
    # Assuming 'number' is a field in Profile
    if Profile.objects.filter(number=number).exists():
        result['number'] = True

    return JsonResponse(result)


@login_required
def profiles_data(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search', '')
    # Filter by skills (assuming the skill filter is a comma-separated list of skill IDs)
    skill_filter = request.GET.get('skills', '')
    state_filter = request.GET.get('states', '')

    profiles = Profile.objects.all()
    if search_value:
        profiles = profiles.filter(
            Q(name__icontains=search_value) |
            Q(surname__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(number__icontains=search_value)
        )

    if skill_filter:
        skill_ids = skill_filter.split(',')
        profiles = profiles.filter(skills__id__in=skill_ids).distinct()

    if state_filter:
        states = state_filter.split(',')
        print("states: ", states)
        profiles = profiles.filter(state__in=states)

    paginator = Paginator(profiles, length)
    profiles_page = paginator.get_page(start // length + 1)

    """
    data = [{
        'id': profile.id,
        'name': profile.name,
        'surname': profile.surname,
        'email': profile.email,
        'number': profile.number,
        'town': profile.town,
        'creation_date': profile.creation_date.strftime('%d/%m/%Y'),
        'update_date': profile.update_date.strftime('%d/%m/%Y %H:%M:%S'),
        'comments': [
            {
                "id": com.id,
                "text": com.text,
                "username": com.user.username,
                "creation_date": com.creation_date.strftime('%d/%m/%Y'),
            } for com in profile.comments.all()
        ],
        'state': profile.state,
        'diplomas': profile.diplomas,
        'skills': list(profile.skills.all().values('id', 'name')),
        'files': [
            {
                'id': f.id,
                'url': f.file.url,
                "file_name": os.path.basename(f.file.name),
            } for f in profile.files.all()
        ]
    } for profile in profiles_page]
    """
    # print("profiles_page: ", profiles_page)
    # print("profiles_page.object_list: ", profiles_page.object_list)
    # .values('id', 'name', 'surname')
    # print("list profiles_page.object_list: ", list(profiles_page.object_list))

    serializer = ProfileSerializer(profiles_page, many=True)

    response = {
        # 'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'profiles': serializer.data,
    }

    return JsonResponse(response, encoder=DjangoJSONEncoder)
