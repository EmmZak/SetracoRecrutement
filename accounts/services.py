from .models import UserGroup
#rom django.contrib.auth.models import Permission, Group


# def _create_groups(group_model: Group, perm_model: Permission):
#     group_model.objects.all().delete()


def create_groups_from_apps(apps):
    """
    creates groups with associated permissions

    args
        apps (comes from Django itself migrations.RunPython(create_groups_from_apps))
    """
    #group_model = Group
    #perm_model = Permission
    #if apps is None:
    #    group_model = Group
    #    perm_model = Permission

    #exit()
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    #Group.objects.all().delete()

    admin_perm_names = [
        'add_user', 'change_user', 'delete_user', 'view_user'  # user
    ]
    perms = Permission.objects.filter(codename__in=admin_perm_names).all()
    print("perms: ", perms)
    group = Group.objects.create(name=UserGroup.ADMIN)
    group.permissions.set(perms)
    group.save()

    consultant_perm_names = [
        'view_comment', 'add_comment',  # comment
        'view_profile', 'change_profile',  # profile
        'view_profilefile',
        'view_skill'
    ]
    perms = Permission.objects.filter(codename__in=consultant_perm_names).all()
    print("perms: ", perms)
    group = Group.objects.create(name=UserGroup.CONSULTANT)
    group.permissions.set(perms)
    group.save()

    editor_perm_names = [
        'view_comment', 'add_comment', 'change_comment', 'delete_comment',  # comment
        'view_profile', 'add_profile', 'change_profile', 'delete_profile',  # profile
        'view_profilefile', 'add_profilefile', 'change_profilefile', 'delete_profilefile',  # profile file
        'view_skill', 'add_skill', 'change_skill', 'delete_skill',  # skill
    ]
    perms = Permission.objects.filter(codename__in=editor_perm_names).all()
    print("perms: ", perms)
    group = Group.objects.create(name=UserGroup.EDITOR)
    group.permissions.set(perms)
    group.save()
