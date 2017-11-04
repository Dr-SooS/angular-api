import json
import random
import string

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import QueryDict
from django.http.response import HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from app.models import UserSession, Task


def signup(request):
    user = User.objects.create_user(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
    user.save()
    session = UserSession.objects.create(session=''.join(random.choices(string.ascii_uppercase + string.digits, k=50)), user=user)
    session.save()
    authenticate(request, username=session.user.username, password=session.user.password)
    login(request, user)
    return JsonResponse({'session': session.session})


def account(request):
    session = UserSession.objects.get(pk=request.GET['session'])
    if session is not None:
        return JsonResponse({'username': session.user.username})
    return HttpResponse(status=404)


def projects(request):
    user = UserSession.objects.get(pk=request.GET['session']).user
    projects_resp = {"projects": []}
    for project in user.projects.all():
        projects_resp["projects"].append({"Project": {"id": project.id, "title": project.title, 'task_count': project.tasks.count()}})
    return JsonResponse(projects_resp)


def tasks(request):
    user = UserSession.objects.get(pk=request.GET['session']).user
    project = user.projects.get(pk=request.GET['project_id'])
    tasks_resp = {"tasks": [], "total_count": project.tasks.count()}
    for task in project.tasks.all():
        tasks_resp["tasks"].append({"Task": {"id": task.id, "title": task.title, "created_at": task.created_at}})
    return JsonResponse(tasks_resp)


class ProjectApi(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectApi, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        user = UserSession.objects.get(pk=request.GET['session']).user
        project = user.projects.get(pk=request.GET['project_id'])
        return JsonResponse({'Project': {'id': project.id, 'title': project.title, 'task_count': project.tasks.count()}})

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        user = UserSession.objects.get(pk=body['session']).user
        project = user.projects.create(title=body['Project']['title'], user=user)
        project.save()
        return JsonResponse({'Project': {'id': project.id}})

    def put(self, request):
        body = json.loads(request.body.decode('utf-8'))
        user = UserSession.objects.get(pk=body['session']).user
        project = user.projects.get(pk=body['Project']['id'])
        project.title = body['Project']['title']
        project.save()
        return JsonResponse({'Project': {'id': project.id, 'title': project.title, 'task_count': project.tasks.count()}})

    def delete(self, request):
        # body = json.loads(request.body.decode('utf-8'))
        # user = UserSession.objects.get(pk=body['session']).user
        # user.projects.get(pk=body['project_id']).delete()
        user = UserSession.objects.get(pk=request.GET['session']).user
        user.projects.get(pk=request.GET['project_id']).delete()
        return HttpResponse(status=200)


class TaskApi(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskApi, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        task = Task.objects.get(pk=request.GET['task_id'])
        return JsonResponse({'Task': {'id': task.id, 'title': task.title, 'description': task.description}})

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        user = UserSession.objects.get(pk=body['session']).user
        project = user.projects.get(pk=body['Project']['id'])
        task = project.tasks.create(title=body['Task']['title'], description=body['Task']['description'])
        task.save()
        return JsonResponse({'Task': {'id': task.id}})

    def put(self, request):
        body = json.loads(request.body.decode('utf-8'))
        task = Task.objects.get(pk=body['Task']['id'])
        task.title = body['Task']['title']
        task.description = body['Task']['description']
        task.save()
        return JsonResponse({'Task': {'id': task.id, 'title': task.title, 'description': task.description}})

    def delete(self, request):
        # body = json.loads(request.body.decode('utf-8'))
        # Task.objects.get(pk=body['task_id']).delete()
        Task.objects.get(pk=request.GET['task_id']).delete()
        return HttpResponse(status=200)
