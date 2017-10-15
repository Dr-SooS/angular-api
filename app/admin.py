from django.contrib import admin

# Register your models here.
from app.models import UserSession, Project, Task

admin.site.register(UserSession)
admin.site.register(Project)
admin.site.register(Task)
