
from django.urls import path


from . import views

app_name = 'Api'
urlpatterns = [
    path('UpdateMark/', views.UpdateMark),
    path('UpdateLessonInfo/', views.UpdateLessonInfo),
    path('UpdateSemestrMark/', views.UpdateSemestrMark),
    path('UpdateSemesterInfo/', views.UpdateSemesterInfo, name='semesterInfo')
]