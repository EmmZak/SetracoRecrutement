from django import forms
from .models import Profile, Comment, ProfileFile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'email',
                  'number', 'town', 'skills', 'diplomas']
        widgets = {
            'skills': forms.CheckboxSelectMultiple(),  # To handle ManyToManyField
            'diplomas': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class ProfileFileForm(forms.ModelForm):
    class Meta:
        model = ProfileFile
        fields = ['file']
