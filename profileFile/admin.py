from django.contrib import admin

from .models import ProfileFile

@admin.register(ProfileFile)
class ProfileFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'file')
    search_fields = ('profile__name', 'profile__surname')
