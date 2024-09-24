from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from SetracoRecrutement.logger import Logger
from config.models import Skill, State

from .forms import CommentForm, ProfileFileForm, ProfileForm
from .models import Comment, Profile, ProfileFile
from django.core.exceptions import PermissionDenied

logger = Logger('profiles')


@login_required
def config(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        return render(request, 'config.html', {'skills': skills})


@permission_required('profiles.view_profile', raise_exception=True)
@login_required
def profiles_view(request):
    is_superuser = request.user.is_superuser

    is_editor_or_admin = request.user.groups.filter(
        name__in=['Editeur', 'Admin']).exists()

    is_editor_or_admin_or_superuser = is_superuser or is_editor_or_admin
    #print("is_editor_or_admin: ", is_editor_or_admin_or_superuser)

    profile_form = ProfileForm()
    profile_file_form = ProfileFileForm()
    comment_form = CommentForm()

    return render(request, 'profiles.html', {'is_editor_or_admin': is_editor_or_admin_or_superuser, "profile_form": profile_form, "profile_file_form": profile_file_form, "comment_form": comment_form})


def has_add_or_change_permission(user):
    if not (user.has_perm('profiles.add_profile') or user.has_perm('profiles.change_profile')):
        raise PermissionDenied  # Raises the exception when permissions are lacking
    return True

@transaction.atomic
@login_required
@user_passes_test(has_add_or_change_permission)
@require_http_methods(["POST"])
def profiles_create(request):
    profile_id = request.POST.get('id')
    try:
        logger.info(
            f"{'Updating' if profile_id else 'Creating'} profile", request=request)
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        town = request.POST.get('town')
        email = request.POST.get('email')
        number = request.POST.get('number')
        diplomas = request.POST.get('diplomas')
        comment = request.POST.get('comment')
        skill_ids = request.POST.get('skills', '')
        state_id = request.POST.get('state', None)
        files = request.FILES.getlist('files')
        logger.debug(
            f"Profile form data: "
            f"surname={surname}, "
            f"name={name}, "
            f"town={town}, "
            f"email={email}, "
            f"number={number}, "
            f"diplomas={diplomas}, "
            f"comment={comment}, "
            f"skill_ids={skill_ids}, "
            f"state_id={state_id}, "
            f"files={len(files)} files uploaded."
        )
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

        for file in files:
            ProfileFile.objects.create(profile=profile, file=file)
    except Exception as e:
        logger.error(f"Error creating profile {e}", request=request)

    return redirect('/profiles')


@login_required
@permission_required('profiles.delete_profile', raise_exception=True)
@require_http_methods(["DELETE"])
def profile_delete(request):
    profile_id = request.GET.get('id')
    logger.info(f"Deleting profile by id: {profile_id}", request=request)
    try:
        if profile_id:
            Profile.objects.filter(id=profile_id).delete()
    except Exception as e:
        logger.error(
            f"Error deleting profile by id: {profile_id} {e}", request=request)

    return redirect('/profiles')


@login_required
def home(request):
    return render(request, 'home.html')
