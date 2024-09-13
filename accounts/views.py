from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.core.serializers import serialize


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

# @login_required
# @user_passes_test(is_admin)


@login_required
def user_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    if not is_admin(request.user):
        return HttpResponseForbidden(render(request, 'perm_denied.html'))

    return render(request, 'users.html')


def groups_data(request):
    groups = list(Group.objects.all().values('id', 'name'))
    print("groups: ", groups)
    response = {
        'groups': groups
    }
    return JsonResponse(response)


def users_data(request):

    users = User.objects.all()

    user_data = [{
        'id': user.id,
        'username': user.username,
        'date_joined': user.date_joined.strftime('%d/%m/%Y'),
        'groups': [{
            'id': group.id,
            'name': group.name
        } for group in user.groups.all()]
    } for user in users]

    response = {
        'users': user_data
    }
    return JsonResponse(response)


@login_required
@user_passes_test(is_admin)
def users_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        group_id = request.POST.get('groups')

        if password != confirm_password:
            print("password not equal")
            error = "Les mots de passent ne sont pas identiques"
            return render(request, 'users.html', {'error': error})

        print("groups: ", group_id)
        group = Group.objects.filter(id=group_id).get()
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.groups.set([group])
        user.save()

    return redirect('/users')


@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE"])
def users_delete(request):
    user_id = request.GET.get('id')
    print("deleting user id: ", user_id)
    if user_id:
        User.objects.filter(id=user_id).delete()

    return redirect('/users')
