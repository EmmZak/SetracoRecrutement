from django import forms

from .models import Skill, State


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class SkillDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm Deletion", required=True)


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name']


class StateDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm Deletion", required=True)
