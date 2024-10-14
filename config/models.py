from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Skill [name: {self.name}]"


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"State [name: {self.name}]"


class Training(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Training [name: {self.name}]"
