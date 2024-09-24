from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.html import format_html


class SingleGroupAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if len(groups) > 1:
            raise forms.ValidationError("Seul un seul groupe doit être choisi")
        return groups


class CustomUserAdmin(UserAdmin):
    form = SingleGroupAdminForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active',
         'is_superuser', 'groups')}),
    )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "groups":
            kwargs['widget'] = forms.SelectMultiple(attrs={'size': '6'})
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

"""
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active',
         'is_superuser', 'groups')}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""
