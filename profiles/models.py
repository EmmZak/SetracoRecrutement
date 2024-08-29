from django.db import models
from skills.models import Skill

class Profile(models.Model):
    STATE_CHOICES = [
        ('new', 'New'),
        ('processing', 'Processing'),
        ('ok', 'OK'),
        ('ko', 'KO'),
    ]
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=20)
    town = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='profiles')
    comment = models.TextField(blank=True)
    diplomas = models.TextField(blank=True)  # Multiline string, use TextField
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='new')

    def __str__(self):
        return f"{self.name} {self.surname}"
