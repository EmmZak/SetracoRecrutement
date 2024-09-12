from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_groups')
def has_groups(user, group_names):
    print("group_names: ", group_names)
    if isinstance(group_names, str):
        group_names = group_names.split(',')
    return user.groups.filter(name__in=group_names).exists()
