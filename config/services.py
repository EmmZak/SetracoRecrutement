from config.models import Skill, State, Training
from django.db.models.functions import Lower


def find_all_skills():
    skills = Skill.objects.all().order_by(Lower('name')).values('id', 'name')
    return skills

def find_all_states():
    states = State.objects.all().order_by(Lower('name')).values('id', 'name')
    return states

def find_all_trainings():
    trainings = Training.objects.all().order_by(Lower('name')).values('id', 'name')
    return trainings