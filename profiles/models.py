from django.db import models
from config.models import Skill, State
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    number = models.CharField(max_length=20)
    town = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='profiles')
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, blank=True)

    diplomas = models.TextField(blank=True)  # Multiline string, use TextField
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

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


class ProfileFile(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='profile_files/')

    def __str__(self):
        return f"File for {self.profile.name} {self.profile.surname}"
