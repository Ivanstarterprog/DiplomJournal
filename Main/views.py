from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .table import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from DiplomJournal import settings

SEMESTER = settings.HALFYEAR


class MarksPage(LoginRequiredMixin, TemplateView):
    template_name = 'Marks.html'

    def get_context_data(self, **kwargs):
        lessons = Lesson.objects.filter(subject=kwargs['subject_num']).order_by('number')
        studentsRaw = Marks.objects.filter(lesson__subject=kwargs['subject_num'])
        subject = SubjectToTeacher.objects.get(id=int(kwargs['subject_num']))
        is_there_diplom = subject.diplom
        teacher = subject.teacher
        students = {}
        for student in studentsRaw:
            marksRaw = Marks.objects.filter(lesson__subject__id=kwargs['subject_num'], student=student.student)
            marks = []
            semesterMark = SemesterMarks.objects.get(subject=kwargs['subject_num'],
                                                     student__student=student.student.student, type='SE')
            for mark in marksRaw:
                marks.append({'id': mark.id, 'mark': mark.mark, 'type': 'Normal'})
            marks.append({'id': semesterMark.id, 'mark': semesterMark.mark, 'type': 'Semester'})
            if lessons[0].subject.diplom:
                semesterMark = SemesterMarks.objects.get(subject=kwargs['subject_num'],
                                                         student__student=student.student.student, type='DI')
                marks.append({'id': semesterMark.id, 'mark': semesterMark.mark, 'type': 'Diplom'})
            students[student.student.student] = marks
        choices = Lesson._meta.get_field('type').choices
        kwargs['choices'] = choices
        kwargs['subject'] = subject
        kwargs['lessons'] = lessons
        kwargs['students'] = students
        kwargs['diplom'] = is_there_diplom
        kwargs['teacher'] = teacher
        return super().get_context_data(**kwargs)



def group_required(*group_names):
    def in_groups(u):
        if u.role in group_names:
            return True
        return redirect('/')

    return user_passes_test(in_groups)


@login_required()
def index(request):
    if request.user.role == 'IT':
        return redirect('Main:workers')
    else:
        return redirect('Main:user', userID=request.user.id)


def login(request):
    return render(request, 'Login.html')


def adminLogin(request):
    return redirect('/login')


@login_required()
@group_required('IT', 'AD', 'TE')
def groups(request):
    table = GroupsTable(Groups.objects.all())
    data = {"table": table, 'title': 'Список групп'}
    return render(request, 'TablePage.html', data)


@login_required()
@group_required('IT', 'AD', 'TE')
def group(request, group_num):
    group = Groups.objects.get(name=group_num)
    table = StudentsTable(StudentToGroup.objects.filter(group__name=group_num))
    semester = SemestersTable(SemesterInfo.objects.filter(group__name=group_num))
    students = len(StudentToGroup.objects.filter(group__name=group_num))
    data = {"students": table,
            'group': group,
            'semester': semester,
            'studentsNum': students}
    return render(request, 'Group.html', data)


@login_required()
@group_required('IT', 'AD', 'TE')
def subjectsMarks(request, group_num, course, yearhalf):
    group = Groups.objects.get(name=group_num)
    table = SubjectsStudentTable(SubjectToTeacher.objects.filter(group=group, course=course, yearhalf=yearhalf))
    data = {
        'group': group,
        'table': table,
        'title': f'Предметы, проходимые группой в {yearhalf} половину {course} курса',
    }
    return render(request, 'TablePage.html', data)


@login_required()
@group_required('IT', 'AD', 'TE')
def teacherPastSubjects(request, userID):
    table = SubjectsTable(
        SubjectToTeacher.objects.filter(teacher__id=userID, active=False))
    data = {
        'group': group,
        'table': table,
        'title': 'Предметы, которые ранее преподавал преподаватель',
    }
    return render(request, 'TablePage.html', data)


@login_required()
@group_required('IT', 'AD', 'TE')
def groupResults(request, group_num, course, yearhalf):
    studentsRaw = StudentToGroup.objects.filter(group__name=group_num)
    students = []
    semesterMarksRaw = SemesterMarks.objects.filter(student=studentsRaw[0], subject__course=course, subject__yearhalf=yearhalf,
                                                    type='SE')
    diplomMarksRaw = SemesterMarks.objects.filter(student=studentsRaw[0], subject__course=course, subject__yearhalf=yearhalf,
                                                  type='DI')
    semesterMarksNames = []
    diplomMarksNames = []
    for marks in semesterMarksRaw:
        semesterMarksNames.append(marks.subject)
    for marks in diplomMarksRaw:
        diplomMarksNames.append(marks.subject)

    for student in studentsRaw:
        semesterMarksRaw = SemesterMarks.objects.filter(student=student, subject__course=course, subject__yearhalf=yearhalf, type='SE')
        diplomMarksRaw = SemesterMarks.objects.filter(student=student, subject__course=course, subject__yearhalf=yearhalf, type='DI')
        semesterMarks = []
        diplomMarks = []
        for mark in semesterMarksRaw:
            semesterMarks.append({'id': mark.id, 'mark': mark.mark})
        for mark in diplomMarksRaw:
            diplomMarks.append({'id': mark.id, 'mark': mark.mark})
        students.append((student.student.get_Fio, semesterMarks, diplomMarks))
    print(diplomMarksNames)
    data = {
        'semesterNames': semesterMarksNames,
        'diplomNames': diplomMarksNames,
        'students': students,
        'semesters': len(semesterMarksNames),
        'diploms': len(diplomMarksNames),
        'course': course,
        'yearhalf': yearhalf
    }
    return render(request, 'Semester.html', data)


@login_required()
def user(request, userID):
    if request.user.id != userID and request.user.role == 'ST':
        return redirect('Main:user', userID=request.user.id)
    userFind = CustomUser.objects.get(id=userID)
    full_name = userFind.get_full_name()
    data = {'userFind': userFind, 'full_name': full_name}
    if userFind.role == 'AD' or userFind.role == 'TE':
        subjects = SubjectsTable(SubjectToTeacher.objects.filter(teacher__id=userFind.id, active=True))
        data['subjects'] = subjects
    if userFind.role == 'ST':
        if StudentToGroup.objects.filter(student=userFind).exists():
            groupInfo = StudentToGroup.objects.get(student=userFind)
            subjects = SubjectsTable(
                SubjectToTeacher.objects.filter(course = groupInfo.group.semester.course, yearhalf=HALFYEAR))
            data['subjects'] = subjects
            data['group'] = groupInfo.group
            data['exist'] = True
        else:
            data['exist'] = False
    if Groups.objects.filter(curator_id=userFind.id):
        curator = Groups.objects.filter(curator_id=userFind.id)
        data['curator'] = curator
    return render(request, 'User.html', context=data)


@login_required()
@group_required('IT', 'AD')
def workers(request):
    work = CustomUser.objects.filter(~Q(role='ST'))
    table = WorkersTable(work)
    data = {
        'table': table,
        'title': 'Список сотрудников колледжа'
    }
    return render(request, 'TablePage.html', context=data)

