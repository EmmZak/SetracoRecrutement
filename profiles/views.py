from django.shortcuts import render
from django.contrib.auth.models import User


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
