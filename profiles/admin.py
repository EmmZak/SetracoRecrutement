from django.contrib import admin

from profileFile.models import ProfileFile
from .models import Profile


class ProfileFileInline(admin.TabularInline):  # or use admin.StackedInline
    model = ProfileFile
    extra = 1  # Number of empty forms to display for adding new ProfileFile objects
    fields = ('file',)
    readonly_fields = ('file',)

@admin.action(description="Mark selected as state=new")
def action_1(modeladmin, request, queryset):
    queryset.update(state="new")

@admin.action(description="Mark selected as state=processing")
def action_2(modeladmin, request, queryset):
    queryset.update(state="processing")

@admin.action(description="Mark selected as state=ok")
def action_3(modeladmin, request, queryset):
    queryset.update(state="ok")

@admin.action(description="Mark selected as state=ko")
def action_4(modeladmin, request, queryset):
    queryset.update(state="ko")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'town', 'state',  'creation_date', 'update_date', 'get_files')
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

    actions = [action_1, action_2, action_3, action_4]

