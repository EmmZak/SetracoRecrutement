from .models import UserGroup
from django.contrib.auth.models import Permission, Group, User


def get_permissions_for_model(model_name, methods):
    """
    args
        model_name: entity name like profile, comment, skill, state
        methos: view, add, delete, change
    """
    if not isinstance(methods, list):
        print("get_permissions_for_model expects a lsit of methods")
        exit()

    model_name = model_name.lower()
    return [f"{method}_{model_name}" for method in methods]


def create_groups_from_apps():
    """
    creates groups with associated permissions
    """
    Group.objects.all().delete()

    admin_perm_names = [
        *get_permissions_for_model('user',
                                   ['add', 'change', 'delete', 'view']),
        *get_permissions_for_model(
            'profile', ['view', 'add', 'change', 'delete']),
        *get_permissions_for_model('profilefile', ['delete']),
        *get_permissions_for_model('comment', ['delete']),
        *get_permissions_for_model('skill', ['view', 'add', 'delete']),
        *get_permissions_for_model('state', ['view', 'add', 'delete']),
    ]
    perms = Permission.objects.filter(codename__in=admin_perm_names).all()
    group = Group.objects.create(name=UserGroup.ADMIN)
    group.permissions.set(perms)
    group.save()

    editor_perm_names = [
        *get_permissions_for_model('user',
                                   ['add', 'change', 'delete', 'view']),
        *get_permissions_for_model('profile',
                                   ['view', 'add', 'change', 'delete']),
        *get_permissions_for_model('profilefile', ['delete']),
        *get_permissions_for_model('skill', ['view', 'add']),
        *get_permissions_for_model('state', ['view', 'add']),
    ]
    perms = Permission.objects.filter(codename__in=editor_perm_names).all()
    group = Group.objects.create(name=UserGroup.EDITOR)
    group.permissions.set(perms)
    group.save()

    consultant_perm_names = [
        *get_permissions_for_model('profile', ['view', 'change']),
        *get_permissions_for_model('skill', ['view']),
        *get_permissions_for_model('state', ['view']),
    ]
    perms = Permission.objects.filter(codename__in=consultant_perm_names).all()
    group = Group.objects.create(name=UserGroup.CONSULTANT)
    group.permissions.set(perms)
    group.save()


def create_test_users():
    # The same code as above to create users and assign groups
    admin_group = Group.objects.get(name=UserGroup.ADMIN)
    editor_group = Group.objects.get(name=UserGroup.EDITOR)
    consultant_group = Group.objects.get(name=UserGroup.CONSULTANT)

    user1, created = User.objects.get_or_create(
        username='admin',
        defaults={'password': 'azertyA1'}
    )
    user1.set_password('azertyA1')
    user1.groups.add(admin_group)
    user1.save()

    user2, created = User.objects.get_or_create(
        username='editeur',
        defaults={'password': 'azertyA1'}
    )
    user2.set_password('azertyA1')
    user2.groups.add(editor_group)
    user2.save()

    user3, created = User.objects.get_or_create(
        username='consultant',
        defaults={'password': 'azertyA1'}
    )
    user3.set_password('azertyA1')
    user3.groups.add(consultant_group)
    user3.save()

    # SUPERUSER
    superuser, created = User.objects.get_or_create(
        username='superuser',
        defaults={'is_superuser': True, 'is_staff': True}
    )
    # Set password (since defaults doesn't work with password hashing)
    superuser.set_password('azertyA1')
    superuser.save()

    print("Test users created with all 3 groups")
