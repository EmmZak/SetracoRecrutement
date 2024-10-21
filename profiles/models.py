from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
import os

from config.models import Skill, State, Training


class Profile(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    number = models.CharField(max_length=20)
    town = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='profiles')
    trainings = models.ManyToManyField(Training, related_name='trainings')
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, blank=True)

    diplomas = models.TextField(blank=True)  # Multiline string, use TextField
    # birthday = models.DateField(null=True, blank=True)
    birthday = models.CharField(max_length=50, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.surname} {self.state} {self.skills} {self.trainings} ...]"


class Comment(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.creation_date}"

class FollowUp(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='followups', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FollowUp by {self.user.username} on {self.creation_date}"

class ProfileFile(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='profile_files/')

    def __str__(self):
        return f"File for {self.profile.name} {self.profile.surname}"

@receiver(models.signals.post_delete, sender=ProfileFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
