from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from SetracoRecrutement.logger import Logger
from config.forms import SkillDeleteForm, SkillForm, StateDeleteForm, StateForm, TrainingForm, TrainingDeleteForm
from config.models import Skill, State, Training
from django.core.exceptions import PermissionDenied
from .services import find_all_states, find_all_skills, find_all_trainings

logger = Logger('config')


def has_skill_state_view_permissions(user):
    if not (user.has_perm('config.view_skill') and user.has_perm('config.view_state')):
        raise PermissionDenied  # Raises the exception when permissions are lacking
    return True


#@user_passes_test(has_skill_state_view_permissions)
@login_required
def config_view(request):
    if request.method == 'GET':
        skills = find_all_skills()
        states = find_all_states()
        trainings = find_all_trainings()

        create_form = SkillForm()
        delete_form = SkillDeleteForm()

        return render(
            request,
            'config.html',
            {
                'skills': skills,
                'states': states,
                'trainings': trainings,
                # 'create_form': create_form,
                # 'delete_form': delete_form
            }
        )


@login_required
# @permission_required('config.add_skill', raise_exception=True)
@require_http_methods(["POST"])
def create_skill(request):
    try:
        logger.info("Creating skill", request=request)
        form = SkillForm(request.POST)
        if form.is_valid():
            logger.info(
                f"Skill form data {form.cleaned_data}", request=request)
            form.save()
    except Exception as e:
        logger.error(f"Error creating skill {e}", request=request)

    return redirect('/config')


@login_required
# @permission_required('config.add_skill', raise_exception=True)
@require_http_methods(["POST"])
def create_training(request):
    try:
        logger.info("Creating training", request=request)
        form = TrainingForm(request.POST)
        if form.is_valid():
            logger.info(
                f"Training form data {form.cleaned_data}", request=request)
            form.save()
    except Exception as e:
        logger.error(f"Error creating training {e}", request=request)

    return redirect('/config')


@login_required
@permission_required('config.add_state', raise_exception=True)
@require_http_methods(["POST"])
def create_state(request):
    try:
        logger.info("Creating state", request=request)
        form = StateForm(request.POST)
        if form.is_valid():
            logger.info(
                f"State form data {form.cleaned_data}", request=request)
            form.save()
    except Exception as e:
        logger.error(f"Error creating state {e}", request=request)

    return redirect('/config')


@permission_required('config.delete_skill', raise_exception=True)
@require_http_methods(["POST"])
def delete_skill(request):
    pk = request.POST.get("pk")
    logger.info(f"Deleting skill by pk: {pk}", request=request)
    try:
        skill = get_object_or_404(Skill, pk=pk)
        form = SkillDeleteForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm']:
            skill.delete()
    except Exception as e:
        logger.error(f"Error deleting {e}", request=request)

    return redirect('/config')

# @permission_required('config.delete_skill', raise_exception=True)


@require_http_methods(["POST"])
def delete_training(request):
    pk = request.POST.get("pk")
    logger.info(f"Deleting training by pk: {pk}", request=request)
    try:
        training = get_object_or_404(Training, pk=pk)
        form = TrainingDeleteForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm']:
            training.delete()
    except Exception as e:
        logger.error(f"Error deleting {e}", request=request)

    return redirect('/config')


@permission_required('config.delete_state', raise_exception=True)
@require_http_methods(["POST"])
def delete_state(request):
    pk = request.POST.get("pk")
    logger.info(f"Deleting state by pk: {pk}", request=request)
    try:
        state = get_object_or_404(State, pk=pk)
        form = StateDeleteForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm']:
            state.delete()
    except Exception as e:
        logger.error(f"Error deleting {e}", request=request)

    return redirect('/config')
