from django import forms
from .models import ProfileFile

class ProfileFileForm(forms.ModelForm):
    class Meta:
        model = ProfileFile
        fields = ['file']
