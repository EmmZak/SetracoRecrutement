from django.db import models
from profiles.models import Profile

class ProfileFile(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='profile_files/')

    def __str__(self):
        return f"File for {self.profile.name} {self.profile.surname}"
