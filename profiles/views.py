from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Skill
from django.views.decorators.http import require_POST


def config(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        return render(request, 'config.html', {'skills': skills})

def add_skill(request):
    if request.method == 'POST':
        # Add a new skill
        skill_name = request.POST.get('skill_name')
        if skill_name:
            Skill.objects.create(name=skill_name)
        return redirect('/config')

@require_POST
def delete_skill(request):
    skill_id = request.POST.get('id')
    if skill_id:
        Skill.objects.filter(id=skill_id).delete()
    return redirect('/config')

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
    side_panel_routes = {
        'Home': '/',
        'Profile': '/profile/',
        'Settings': '/settings/',
        'About': '/about/',
    }
    return render(request, 'home.html', {'side_panel_routes': side_panel_routes})


def profiles_view(request):
    return render(request, 'profiles.html')

# users


def users_view(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})
