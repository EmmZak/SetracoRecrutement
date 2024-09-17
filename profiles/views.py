from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from config.models import Skill, State
from .forms import ProfileForm, CommentForm, ProfileFileForm
from .models import Profile, Comment, ProfileFile
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction


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

    profile_form = ProfileForm()
    profile_file_form = ProfileFileForm()
    comment_form = CommentForm()

    return render(request, 'profiles.html', {'is_editor_or_admin': is_editor_or_admin_or_superuser, "profile_form": profile_form, "profile_file_form": profile_file_form, "comment_form": comment_form})


@require_http_methods(["POST"])
def profiles_create_form(request):
    print("here")
    profile_form = ProfileForm(request.POST)
    profile_file_form = ProfileFileForm(request.POST, request.FILES)
    comment_form = CommentForm(request.POST)

    if profile_form.is_valid() and profile_file_form.is_valid() and comment_form.is_valid():
        profile = profile_form.save()
        profile_file = profile_file_form.save(commit=False)
        profile_file.profile = profile
        profile_file.save()

        comment = comment_form.save(commit=False)
        comment.profile = profile
        comment.user = request.user  # Assuming the user is logged in
        comment.save()
    else:
        print("forms not valid")

    return redirect('/profiles')


@transaction.atomic
@login_required
@require_http_methods(["POST"])
def profiles_create(request):

    profile_id = request.POST.get('id')
    surname = request.POST.get('surname')
    name = request.POST.get('name')
    town = request.POST.get('town')
    email = request.POST.get('email')
    number = request.POST.get('number')
    diplomas = request.POST.get('diplomas')
    comment = request.POST.get('comment')
    skill_ids = request.POST.get('skills', '')
    state_id = request.POST.get('state', None)
    profile = get_object_or_404(
        Profile, id=profile_id) if profile_id else Profile()

    profile.surname = surname
    profile.name = name
    profile.town = town
    profile.email = email
    profile.number = number
    profile.diplomas = diplomas
    profile.state = State.objects.filter(
        id=state_id).first() if state_id else None
    profile.save()

    if comment:
        Comment.objects.create(
            profile=profile,
            user=request.user,
            text=comment
        )

    if skill_ids:
        selected_skill_ids = list(map(int, skill_ids.split(',')))
        selected_skills = Skill.objects.filter(id__in=selected_skill_ids)
        profile.skills.set(selected_skills)
    else:
        profile.skills.clear()

    for file in request.FILES.getlist('files'):
        ProfileFile.objects.create(profile=profile, file=file)

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
