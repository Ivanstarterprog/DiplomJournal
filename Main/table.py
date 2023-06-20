from __future__ import absolute_import, unicode_literals

import django_tables2 as tables
from django.forms import forms
from django.utils.html import format_html
from django_tables2 import Column
from .models import *
from django.utils.safestring import mark_safe
from django_tables2.utils import AttributeDict
import warnings


class GroupsTable(tables.Table):
    name = tables.URLColumn(linkify=lambda record: 'group/' + str(record.name))
    curator = tables.URLColumn(linkify=lambda record: 'user/' + str(record.curator.id))

    class Meta:
        model = Groups
        fields = ("speciality", "name", 'course', 'curator')
        template_name = "django_tables2/bootstrap.html"


class WorkersTable(tables.Table):
    get_full_name = tables.TemplateColumn(
        '{% if record.role != "IT"%}<a href="{% url "Main:user" userID=record.id %}"> {{ record.get_full_name }} '
        '</a>{% else %}'
        '{{ record.get_full_name }} {%endif%}', verbose_name='ФИО')

    class Meta:
        model = CustomUser
        fields = ('get_full_name', 'role', 'num', 'address', 'birthday', 'floor')


class SubjectsTable(tables.Table):
    subject = tables.TemplateColumn(
        '<a href="{% url "Main:marksSubject" group_num=record.group.name subject_num=record.id%}"> {{ record}} </a>')
    test = tables.TemplateColumn(template_code="{{ record.course }} курс, {{ record.semester}} семестр",
                                 verbose_name='Курс, семестр')  #

    class Meta:
        model = SubjectToTeacher
        fields = ("group", "subject", 'hours', 'test',)
        exlcude = ('id', 'teacher',)


class SubjectsStudentTable(tables.Table):
    subject = tables.TemplateColumn(
        '<a href="{% url "Main:marksSubject" group_num=record.group.name subject_num=record.id%}"> {{ record}} </a>')

    class Meta:
        model = SubjectToTeacher
        fields = ("subject", 'hours',  'teacher')
        exlcude = ('id', 'teacher',)


class SemestersTable(tables.Table):
    current = tables.TemplateColumn(template_code="{{ record.course }} курс, {{ record.yearhalf}} семестр",
                                 verbose_name='Курс, семестр')
    weeks = tables.TemplateColumn('{% if user.role == "IT" or user.role == "AD"%}<input type="number" min="0" value="{{record.weeks}}" '
                                  'id="{{ record.id }}_weeks" oninput="UpdateSemesterInfo(this, {{ record.id }})">{% else %}'
        '{{record.weeks}}{% endif %}')
    subjects = tables.TemplateColumn(
        '<a href="{% url "Main:groupSubjects" group_num=record.group.name course=record.course '
        'yearhalf=record.yearhalf %}">Список предметов</a>', verbose_name='Предметы')
    startdate = tables.TemplateColumn(
        '{% if user.role == "IT" or user.role == "AD"%} <input name="{{ record.startdate }}" id="{{record.id}}_startdate" oninput="UpdateSemesterInfo(this, {{ record.id }})"'
        ' type="date" value="{{record.startdate|date:"Y-m-d"}}">{% else %}'
        '{{record.startdate}}{% endif %}'
    )
    rubej = tables.TemplateColumn(
        '{% if user.role == "IT" or user.role == "AD"%}<input id="{{record.id}}_rubej" oninput="UpdateSemesterInfo(this, {{ record.id }})"'
        'type="date" value="{{record.rubej|date:"Y-m-d"}}"{% else %}">{{record.rubej}}{% endif %}'
    )
    results = tables.TemplateColumn(
        '<a href="{% url "Main:semesterMarks" group_num=record.group.name course=record.course '
        'yearhalf=record.yearhalf %}">Сводная ведомость за '
        'семестр</a>', verbose_name='Ведомость'
    )
    class Meta:
        model = SemesterInfo
        fields = (
            'current', 'subjects', 'weeks', 'startdate', 'rubej', 'results'
        )

class StudentsTable(tables.Table):
    student = tables.URLColumn(linkify=lambda record: '../../user/' + str(record.student.id))

    class Meta:
        model = StudentToGroup
        fields = (
            'student', 'student__num', 'student__birthday', 'student__floor', 'zachotka', 'health'
        )

