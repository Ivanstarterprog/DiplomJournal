import datetime
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig

from Main.models import *
from Main.table import GroupsTable


# Create your views here.

@csrf_exempt
def UpdateMark(request):
    if request.method == 'POST':
        print(request.POST.get('markID'))
        markId = Marks.objects.get(id=request.POST.get('markID'))
        newMark = request.POST.get('newMark')
        markId.mark = newMark
        markId.save()
        return HttpResponse(status=204)


@csrf_exempt
def UpdateLessonInfo(request):
    if request.method == 'POST':
        lessonID = request.POST.get('lessonID')
        date = request.POST.get('date')
        type = request.POST.get('type')
        topic = request.POST.get('topic')
        task = request.POST.get('task')
        if date == '':
            date = None
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        Lesson.objects.filter(id=lessonID).update(
            date=date,
            type=type,
            topic=topic,
            independentTask=task
        )

        return HttpResponse(status=204)


@csrf_exempt
def UpdateSemesterInfo(request):
    print('dwadwads')
    if request.method == 'POST':
        semesterID = request.POST.get('semesterID')
        startdate = request.POST.get('startdate')
        rubej = request.POST.get('rubej')
        weeks = request.POST.get('weeks')
        if startdate == '':
            startdate = None
        else:
            startdate = datetime.datetime.strptime(str(startdate), "%Y-%m-%d").date()
        if rubej == '':
            rubej = None
        else:
            rubej = datetime.datetime.strptime(str(rubej), "%Y-%m-%d").date()

        SemesterInfo.objects.filter(id=semesterID).update(
            rubej=rubej,
            startdate=startdate,
            weeks=weeks
        )

        return HttpResponse(status=204)


@csrf_exempt
def UpdateSemestrMark(request):
    if request.method == 'POST':
        print(request.POST.get('markID'))
        newMark = request.POST.get('newMark')
        SemesterMarks.objects.filter(id=request.POST.get('markID')).update(
            mark=newMark
        )
        return HttpResponse(status=204)
