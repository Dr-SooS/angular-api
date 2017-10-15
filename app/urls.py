from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/', views.signup, name="signup"),
    url(r'^account/', views.account, name="account"),
    url(r'^projects/$', views.projects),
    url(r'^projects/project', views.ProjectApi.as_view()),
    url(r'^tasks/$', views.tasks),
    url(r'^tasks/task', views.TaskApi.as_view()),
]