from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Perm = apps.get_model('auth', 'Permission')

    Group.objects.all().delete()

    # exit()
    admin_perm_names = [
        'add_user', 'change_user', 'delete_user', 'view_user'  # user
    ]
    perms = Perm.objects.filter(codename__in=admin_perm_names).all()
    group, _ = Group.objects.get_or_create(name='Admin')
    group.permissions.set(perms)
    group.save()

    consultant_perm_names = [
        'view_comment', 'add_comment',  # comment
        'view_profile', 'change_profile',  # profile
        'view_profilefile',
        'view_skill'
    ]
    perms = Perm.objects.filter(codename__in=consultant_perm_names).all()
    group, _ = Group.objects.get_or_create(name='Consultant')
    group.permissions.set(perms)
    group.save()

    editor_perm_names = [
        'view_comment', 'add_comment', 'change_comment', 'delete_comment',  # comment
        'view_profile', 'add_profile', 'change_profile', 'delete_profile',  # profile
        'view_profilefile', 'add_profilefile', 'change_profilefile', 'delete_profilefile',  # profile file
        'view_skill', 'add_skill', 'change_skill', 'delete_skill',  # skill
    ]
    perms = Perm.objects.filter(codename__in=editor_perm_names).all()
    group, _ = Group.objects.get_or_create(name='Editeur')
    group.permissions.set(perms)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]