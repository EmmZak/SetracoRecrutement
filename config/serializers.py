
from django.db import models
from rest_framework import serializers

from .models import Skill, State, Training


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['id', 'name']