from config.models import Skill, State
from django.db.models.functions import Lower


def find_all_skills():
    skills = Skill.objects.all().order_by(Lower('name')).values('id', 'name')
    return skills

def find_all_states():
    states = State.objects.all().order_by(Lower('name')).values('id', 'name')
    return states