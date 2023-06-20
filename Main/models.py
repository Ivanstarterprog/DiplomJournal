import math

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from ondelta.models import OnDeltaMixin
from DiplomJournal import settings

HALFYEAR = settings.HALFYEAR


class CustomUser(AbstractUser, OnDeltaMixin):
    third_name = models.CharField(max_length=100, default='', verbose_name='Отчество', null=True)
    IT = "IT"
    TEACHER = "TE"
    STUDENT = "ST"
    ADMINISTRATION = "AD"
    ROLES_CHOICES = [
        (IT, "Программист"),
        (TEACHER, "Преподаватель"),
        (STUDENT, "Студент"),
        (ADMINISTRATION, "Администрация"),
    ]
    num = models.CharField(max_length=11, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=300, null=True, verbose_name='Адрес проживания')
    birthday = models.DateField(verbose_name='Дата Рождения', null=True)
    MALE = "MA"
    FEMALE = 'FE'
    FLOORS = [(MALE, "Мужской"), (FEMALE, "Женский")]
    floor = models.CharField(max_length=2, choices=FLOORS, verbose_name='Пол', null=True, default=None)
    role = models.CharField(max_length=2, choices=ROLES_CHOICES, verbose_name='Роль', null=True, default=STUDENT)

    def ondelta_role(self, old_value, new_value):
        if new_value == 'IT' or self.username == 'IvanNurgazin':
            self.is_superuser = True
        else:
            self.is_superuser = False

    @admin.display(description='ФИО')
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.third_name}"

    @property
    def get_Fio(self):
        return f"{self.last_name} {self.first_name[0]}.{self.third_name[0]}"

    def __str__(self):
        return self.get_full_name()


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400, db_index=True, verbose_name='Название предмета')
    shortName = models.CharField(max_length=100, verbose_name='Сокращённое название предмета')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предметы'
        verbose_name_plural = 'Предметы'


class Groups(OnDeltaMixin):
    id = models.AutoField(primary_key=True)
    speciality = models.ForeignKey('Speciality', on_delete=models.PROTECT, db_index=True, null=True,
                                   verbose_name='Специальность')
    name = models.IntegerField(db_index=True, verbose_name='Номер группы')
    limit_choices_to = Q(role='TE') | Q(role='AD')
    curator = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True,
                                related_name='CustomUser_groups_curator',
                                verbose_name='Куратор', limit_choices_to=limit_choices_to)
    semester = models.ForeignKey('SemesterInfo', on_delete=models.SET_NULL, null=True,
                                 verbose_name='Текущий семестр', blank=True)
    OCHNOYE = 'OC'
    ZAOCHNOYE = 'ZA'
    OTDEL = [
        (OCHNOYE, 'Очное'),
        (ZAOCHNOYE, 'Заочное')
    ]
    otdel = models.CharField(max_length=2, verbose_name='Отделение', choices=OTDEL, null=True)
    start_year = models.DateField(default=now, verbose_name='Дата зачисления группы')

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            for course in range(1, self.speciality.years+1):
                SemesterInfo.objects.create(
                    group=self,
                    course=course,
                    semester=1
                )
                SemesterInfo.objects.create(
                    group=self,
                    course=course,
                    semester=2
                )
            SemesterInfo.objects.create(
                group=self,
                course=self.speciality.years+1,
                semester=1
            )
            if self.speciality.months >6:
                SemesterInfo.objects.create(
                    group=self,
                    course=self.speciality.years+1,
                    semester=2
                )
            self.semester = SemesterInfo.objects.get(group=self, course=1, semester=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.speciality.shortName}{str(self.name)}'

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'


class SemesterInfo(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey('Groups', db_index=True, on_delete=models.CASCADE, verbose_name='Группа')
    course = models.PositiveIntegerField(verbose_name='Курс', default=1, db_index=True)
    yearhalf = models.PositiveIntegerField(default=1, verbose_name='Семестр', db_index=True, validators=[
        MaxValueValidator(2),
        MinValueValidator(1)
    ])
    weeks = models.PositiveIntegerField(verbose_name='Количество недель', default=17)
    startdate = models.DateField(verbose_name='Дата начала семестра', default=now)
    rubej = models.DateField(verbose_name='Дата рубежа', default=now)

    @property
    def current(self):
        return f'{self.course} курс, {self.yearhalf} семестр'

    def __str__(self):
        return self.current

    class Meta:
        verbose_name = 'Информация о семестрах'
        verbose_name_plural = 'Информация о семестрах'


class StudentToGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey('Groups', db_index=True, on_delete=models.CASCADE, verbose_name='Группа')
    student = models.OneToOneField('CustomUser', on_delete=models.CASCADE, verbose_name='Студент',
                                limit_choices_to={'role': 'ST'}, db_index=True)
    zachotka = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Номер зачётки', null=True)
    MAINHEALTH = 'MA'
    SPECIAL = 'SP'
    PODGOTOV = 'PO'
    HEALTH_CHOICES = [
        (MAINHEALTH, 'Основная'),
        (SPECIAL, 'Специальная'),
        (PODGOTOV, 'Подготовительная')
    ]
    health = models.CharField(max_length=2, verbose_name='Группа здоровья', choices=HEALTH_CHOICES, default=MAINHEALTH)

    def __str__(self):
        return f'Обучающийся {self.student.get_full_name()} из группы {self.group.name}'

    class Meta:
        verbose_name = 'Студенты в группах'
        verbose_name_plural = 'Студенты в группах'


class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8, db_index=True, verbose_name='Шифр специальности')
    name = models.CharField(max_length=70, db_index=True, verbose_name='Наименование специальности')
    shortName = models.CharField(max_length=30, verbose_name='Сокращённое наименование специальности', default='')
    years = models.PositiveIntegerField(default=3, verbose_name='Годы обучения')
    months = models.PositiveIntegerField(default=10, verbose_name='Месяцы обучения')

    @admin.display(description='Время обучения')
    def get_Time(self):
        return f'{self.years} лет, {self.months} месяцев'

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Специальности'
        verbose_name_plural = 'Специальности'


class SubjectToTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    limit_choices_to = Q(role='TE') | Q(role='AD')
    teacher = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, verbose_name='Преподаватель',
                                db_index=True, limit_choices_to=limit_choices_to)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True, verbose_name='Предмет', db_index=True)
    hours = models.PositiveIntegerField(verbose_name='Часы', default=1)
    group = models.ForeignKey('Groups', on_delete=models.CASCADE, null=True, verbose_name='Группа', db_index=True)
    course = models.PositiveIntegerField(verbose_name='Курс', default=1, null=True)
    yearhalf = models.PositiveIntegerField(verbose_name='Полугодие', default=1, null=True)
    diplom = models.BooleanField(default=False, verbose_name='Оценка идёт в диплом')
    active = models.BooleanField(default=False, verbose_name='Предмет преподаётся в данный момент')

    def ondelta_diplom(self, old_value, new_value):
        diplomMarks = SemesterMarks.objects.filter(subject=self, type='DI')
        students = StudentToGroup.objects.filter(group=self.group)
        if new_value is True and len(diplomMarks) == 0:
            for student in students:
                SemesterMarks.objects.create(
                    subject=self,
                    student=student,
                    type='DI'
                )
        elif new_value is False and len(diplomMarks) != 0:
            SemesterMarks.objects.filter(
                subject=self,
                type='DI'
            ).delete()

    EXAM = 'EX'
    ZACHOT = 'ZA'
    DIFZACHOT = "DZ"
    OTHER = 'OT'
    TYPE_CHOICES = [
        (EXAM, "Экзамен"),
        (ZACHOT, 'Зачёт'),
        (DIFZACHOT, 'Диффиринцированный зачёт'),
        (OTHER, 'Иные формы контроля')
    ]
    type = models.CharField(max_length=2, verbose_name='Форма аттестации', choices=TYPE_CHOICES, default=OTHER)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            number = 0
            for num in range(1, math.ceil(self.hours / 2) + 1):
                Lesson.objects.create(
                    subject=self,
                    group=self.group,
                    number=num
                )
                number = num
            for num in range(2):
                Lesson.objects.create(
                    subject=self,
                    group=self.group,
                    topic='Запасное занятие',
                    number=number
                )
                number += 1
            students = StudentToGroup.objects.filter(group=self.group)
            for student in students:
                SemesterMarks.objects.create(
                    subject=self,
                    student=student,
                    type='SE'
                )
            if self.diplom:
                for student in students:
                    SemesterMarks.objects.create(
                        subject=self,
                        student=student,
                        type='DI'
                    )
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.subject.name}'

    class Meta:
        verbose_name = 'Соотношение предметов и педагогов'
        verbose_name_plural = 'Соотношение предметов и педагогов'


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('SubjectToTeacher', on_delete=models.CASCADE, null=True, verbose_name='Предмет',
                                db_index=True)
    group = models.ForeignKey('Groups', db_index=True, on_delete=models.CASCADE, verbose_name='Группа')
    date = models.DateField(default=None, verbose_name='Дата проведения занятия', null=True, db_index=True, blank=True)
    topic = models.CharField(max_length=125, verbose_name='Тема занятия', null=True, default='')
    independentTask = models.CharField(max_length=500, verbose_name='Задание для работы в классе', null=True,
                                       blank=True, default='')
    number = models.PositiveIntegerField(default=1, verbose_name='Номер занятия', editable=False)
    FULLTZ = 'FT'
    FULLPZ = 'FP'
    HALFTZ = 'HT'
    HALFPZ = 'HP'
    FIFTYFIFTY = 'FF'
    TYPES = [
        (FULLPZ, '2 ПЗ'),
        (FULLTZ, '2 ТЗ'),
        (HALFPZ, '1 ПЗ'),
        (HALFTZ, '1 ТЗ'),
        (FIFTYFIFTY, '1 ТЗ, 1 ПЗ')
    ]
    type = models.CharField(max_length=2, default=FIFTYFIFTY, verbose_name='Тип занятия', null=True, choices=TYPES)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            students = StudentToGroup.objects.filter(group=self.group)
            for student in students:
                Marks.objects.create(
                    lesson=self,
                    student=student
                )
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Занятия'
        verbose_name_plural = 'Занятия'


class Marks(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='Занятие', null=True)
    student = models.ForeignKey('StudentToGroup', on_delete=models.CASCADE, verbose_name='Студент')
    mark = models.CharField(max_length=3, verbose_name='Оценка', default='')

    class Meta:
        verbose_name = 'Оценки'
        verbose_name_plural = 'Оценки'
        unique_together = ['lesson', 'student']


class SemesterMarks(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('StudentToGroup', on_delete=models.CASCADE, verbose_name='Студент', null=True)
    subject = models.ForeignKey('SubjectToTeacher', on_delete=models.CASCADE, verbose_name='Предмет')
    mark = models.CharField(max_length=10, verbose_name='Оценка', default='')
    SEMESTR = 'SE'
    DIPLOM = 'DI'
    TYPE_CHOICES = [
        (SEMESTR, 'Семестр'),
        (DIPLOM, 'Диплом')
    ]
    type = models.CharField(max_length=2, verbose_name='Тип оценки', default=SEMESTR, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'Оценки за семестр'
        verbose_name_plural = 'Оценки за семестр'
