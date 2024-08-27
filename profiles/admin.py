from django.contrib import admin
from .models import Profile, Skill, ProfileFile

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProfileFileInline(admin.TabularInline):  # or use admin.StackedInline
    model = ProfileFile
    extra = 1  # Number of empty forms to display for adding new ProfileFile objects
    fields = ('file',)
    readonly_fields = ('file',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'town', 'state', 'creation_date', 'update_date', 'get_files')
    list_filter = ('state', 'town', 'creation_date', 'update_date')
    search_fields = ('name', 'surname', 'email', 'town')
    ordering = ('-creation_date',)
    filter_horizontal = ('skills',)
    inlines = [ProfileFileInline]  # Add the inline here

    def get_files(self, obj):
        files = obj.files.all()
        if files:
            return ", ".join([file.file.name.split('/')[-1] for file in files])
        return "No files"
    get_files.short_description = 'Files'

@admin.register(ProfileFile)
class ProfileFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'file')
    search_fields = ('profile__name', 'profile__surname')
