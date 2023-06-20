from django.contrib.auth.views import LogoutView
from django.urls import path, include
from wildewidgets import WildewidgetDispatch

from . import views
from django.contrib.auth import views as auth_views

from .forms import CustomAuthForm

app_name = 'Main'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthForm),
         name='login'),
    path('workers', views.workers, name='workers'),
    path('groups', views.groups, name='groups'),
    path("logout", LogoutView.as_view(), name="logout"),
    path("group/<int:group_num>/", views.group, name='group'),
    path("group/<int:group_num>/subjects/<int:course>/<int:yearhalf>", views.subjectsMarks, name='groupSubjects'),
    path("group/<int:group_num>/<int:subject_num>", views.MarksPage.as_view(), name='marksSubject'),
    path("group/<int:group_num>/results/<int:course>/<int:yearhalf>", views.groupResults, name='semesterMarks'),
    path("user/<int:userID>", views.user, name='user'),
    path("user/<int:userID>/pastSubjects", views.teacherPastSubjects, name='teacherPastSubjects')
]
