from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from profileFile.models import ProfileFile
from skills.models import Skill
from .models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.views.decorators.http import require_http_methods
from .models import ProfileForm


def config(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        return render(request, 'config.html', {'skills': skills})


@require_http_methods(["DELETE"])
def profile_delete(request):
    profile_id = request.GET.get('id')
    if profile_id:
        Profile.objects.filter(id=profile_id).delete()
    return redirect('/profiles')


def profiles_view(request):
    return render(request, 'profiles.html')


def profiles_data(request):
    # return render(request, 'profiles.html')
    # draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search', '')
    # Filter by skills (assuming the skill filter is a comma-separated list of skill IDs)
    skill_filter = request.GET.get('skills', '')

    print("start: ", start)
    print("search_value: ", search_value)
    print("skill_filter: ", skill_filter)

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


def profiles_create(request):
    print("here")

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
            comment=comment,
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
            comment=comment,
            state=state
        )

    if profile_id:
        profile = Profile.objects.filter(id=profile_id).first()
    else:
        profile = new_profile

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
