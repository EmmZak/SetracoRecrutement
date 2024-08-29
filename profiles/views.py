from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from skills.models import Skill
from .models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
import os


def config(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        return render(request, 'config.html', {'skills': skills})


def profiles_view(request):
    return render(request, 'profiles.html')


def profiles_data(request):
    # return render(request, 'profiles.html')
    # draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
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
            Q(email__icontains=search_value)
        )

    # Filter by skills (assuming the skill filter is a comma-separated list of skill IDs)
    skill_filter = request.GET.get('skills', '')
    if skill_filter:
        skill_ids = skill_filter.split(',')
        profiles = profiles.filter(skills__id__in=skill_ids).distinct()

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
        'comment': profile.comment,
        'state': profile.state,
        'diplomas': profile.diplomas,
        'skills': [
            {
                "id": skill.id,
                "name": skill.name
            } for skill in profile.skills.all()
        ],
        'files': [
            {
                'id': f.id,
                'url': f.file.url,
                "file_name": os.path.basename(f.file.name),
            } for f in profile.files.all()
        ]
    } for profile in profiles_page]

    response = {
        # 'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'profiles': data,
    }

    return JsonResponse(response)


def profiles_create(requset):
    pass


def users_view(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def test(request):
    items = [
        {
            'name': 'African Elephant',
            'species': 'Loxodonta africana',
            'diet': 'Herbivore',
            'habitat': 'Savanna, Forests',
        },
        # ... more items
    ]
    context = {
        'items': items,
        # 'nb_elements': nb_elements,
        # 'items_per_page': items_per_page,
        # 'page': page,
    }
    return render(request, 'test.html', context)


def home(request):
    return render(request, 'home.html')
