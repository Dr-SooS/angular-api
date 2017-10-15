from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserSession(models.Model):
    user = models.OneToOneField(User)
    session = models.CharField(max_length=50, primary_key=True)


class Project(models.Model):
    user = models.ForeignKey(User, related_name="projects")
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name="tasks")

    def __str__(self):
        return self.title
