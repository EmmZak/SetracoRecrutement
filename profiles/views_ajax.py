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


@require_http_methods(["DELETE"])
def delete_comment(request):
    com_id = request.GET.get('id')
    print("deleting comment: ", com_id)
    if com_id:
        Comment.objects.filter(id=com_id).delete()
        print("returning success")
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def export_profiles_csv(request):
    # Get pagination parameters from the request
    page = int(request.GET.get('page', 1))  # Default to page 1
    # Default to 50 items per page
    items_per_page = int(request.GET.get('itemsPerPage', 50))

    # Fetch the paginated data (adjust query according to your needs)
    profiles = Profile.objects.all()[(
        page - 1) * items_per_page: page * items_per_page]

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

        writer.writerow([
            profile.name, profile.surname, profile.email, profile.number, profile.town,
            skills, profile.diplomas, profile.creation_date, profile.update_date, profile.get_state_display(), comments
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

    # order_column = request.GET.get('order[0][column]', '0')
    # order_direction = request.GET.get('order[0][dir]', 'asc')

    # Define the column index to column name mapping
    # column_names = [
    #     'creation_date',
    #     'update_date',
    #     'town',
    #     'name',
    #     'surname',
    #     'email',
    #     'number'
    # ]
    # Get the column to sort by
    # order_by = columns.get(int(order_column), 'creation_date')
    # if order_direction == 'desc':
    #    order_by = f'-{order_by}'

    # Filter by search term
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
    # Order the queryset
    # profiles = profiles.order_by(order_by)

    # Paginate the results
    paginator = Paginator(profiles, length)
    profiles_page = paginator.get_page(start // length + 1)

    data = [{
        'id': profile.id,
        'name': profile.name,
        'surname': profile.surname,
        'email': profile.email,
        'number': profile.number,
        'town': profile.town,
        'creation_date': profile.creation_date.strftime('%d/%m/%Y'),
        # 'creation_date': profile.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
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

    # print("profiles_page: ", profiles_page)
    # print("profiles_page.object_list: ", profiles_page.object_list)
    # .values('id', 'name', 'surname')
    # print("list profiles_page.object_list: ", list(profiles_page.object_list))

    response = {
        # 'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'profiles': data,
    }

    return JsonResponse(response)

