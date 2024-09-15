from django.db import models
from rest_framework import serializers

# Create your models here
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


