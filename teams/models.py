from django.db import models

from user.models import User


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name
