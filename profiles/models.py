from django.db import models
from config.models import Skill, State
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
    # STATE_TO_VERIFY = "STATE_TO_VERIFY"
    # STATE_VERIFIED = "STATE_VERIFIED"
    # STATE_CONSULTED = "STATE_CONSULTED"
    # STATE_HIRED = "STATE_HIRED"
    # STATE_REJECTED = "STATE_REJECTED"

    # STATE_CHOICES = [
    #     (STATE_TO_VERIFY, STATE_TO_VERIFY),
    #     (STATE_VERIFIED, STATE_VERIFIED),
    #     (STATE_CONSULTED, STATE_CONSULTED),
    #     (STATE_HIRED, STATE_HIRED),
    #     (STATE_REJECTED, STATE_REJECTED),
    # ]
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    number = models.CharField(max_length=20)
    town = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='profiles')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=True)

    # comment = models.TextField(blank=True)
    diplomas = models.TextField(blank=True)  # Multiline string, use TextField
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # state = models.CharField(max_length=20, choices=STATE_CHOICES, default=STATE_TO_VERIFY)

    def __str__(self):
        return f"{self.name} {self.surname} {self.state}]"


class Comment(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.creation_date}"
