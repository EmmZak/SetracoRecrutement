from django.shortcuts import get_object_or_404, render
from config.forms import SkillDeleteForm, SkillForm, StateDeleteForm, StateForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from config.models import Skill, State
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

def has_skill_state_view_permissions(user):
    return user.has_perm('config.view_skill') and user.has_perm('config.view_state')

@user_passes_test(has_skill_state_view_permissions)
@login_required
def config_view(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        states = State.objects.all()

        create_form = SkillForm()
        delete_form = SkillDeleteForm()

        return render(
            request,
            'config.html',
            {'skills': skills, 'states': states,
                'create_form': create_form, 'delete_form': delete_form}
        )


@login_required
@permission_required('config.add_skill', raise_exception=True)
@require_http_methods(["POST"])
def create_skill(request):
    form = SkillForm(request.POST)
    if form.is_valid():
        print("create skill form valid")
        form.save()

    return redirect('/config')
    # return render(request, 'create_skill.html', {'form': form})

@login_required
@permission_required('config.add_state', raise_exception=True)
@require_http_methods(["POST"])
def create_state(request):
    form = StateForm(request.POST)
    if form.is_valid():
        print("create state form valid")
        form.save()

    return redirect('/config')


@permission_required('config.delete_skill', raise_exception=True)
@require_http_methods(["POST"])
def delete_skill(request):
    pk = request.POST.get("pk")
    skill = get_object_or_404(Skill, pk=pk)

    form = SkillDeleteForm(request.POST)

    if form.is_valid() and form.cleaned_data['confirm']:
        skill.delete()

    return redirect('/config')


@permission_required('config.delete_state', raise_exception=True)
@require_http_methods(["POST"])
def delete_state(request):
    pk = request.POST.get("pk")
    state = get_object_or_404(State, pk=pk)

    form = StateDeleteForm(request.POST)

    if form.is_valid() and form.cleaned_data['confirm']:
        state.delete()

    return redirect('/config')
