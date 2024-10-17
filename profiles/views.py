from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from SetracoRecrutement.logger import Logger
from config.models import Skill, State, Training

from .models import Comment, Profile, ProfileFile
from django.core.exceptions import PermissionDenied

logger = Logger('profiles')


def error_page(request):
    error_message = request.GET.get('message', 'Erreur inconnue')
    return render(request, 'error.html', {'error_message': error_message})


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

    return render(request, 'profiles.html', {'is_editor_or_admin': is_editor_or_admin_or_superuser})


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
        birthday = request.POST.get('birthday')
        diplomas = request.POST.get('diplomas')
        comment = request.POST.get('comment')
        skill_ids = request.POST.get('skills', '')
        training_ids = request.POST.get('trainings', '')
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
            f"training_ids={training_ids}, "
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
        profile.birthday = birthday
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

        if training_ids:
            selected_training_ids = list(map(int, training_ids.split(',')))
            selected_trainings = Training.objects.filter(id__in=selected_training_ids)
            profile.trainings.set(selected_trainings)
        else:
            profile.trainings.clear()

        for file in files:
            ProfileFile.objects.create(profile=profile, file=file)
    except Exception as e:
        logger.error(f"Error creating profile {e}", request=request)
        return render(request, 'error.html', {'error_message': "Erreur lors de la création/mise à jour du profile"})

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
