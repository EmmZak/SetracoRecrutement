from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseForbidden

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

#@login_required
#@user_passes_test(is_admin)
def user_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    if not is_admin(request.user):
        return HttpResponseForbidden(render(request, 'perm_denied.html'))

    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign the appropriate group here if needed
            group = Group.objects.get(name='consultant')  # Or 'editor'
            user.groups.add(group)
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/user_form.html', {'form': form})


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
@require_http_methods(["POST"])
def delete_user(request):
    user_id = request.POST.get('id')
    if user_id:
        User.objects.filter(id=user_id).delete()

    return redirect('/users')
