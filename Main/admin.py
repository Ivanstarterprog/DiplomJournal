from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'get_full_name', 'role', 'address', 'num', 'birthday', 'floor']
    list_editable = ['role', 'floor']
    field = UserAdmin.fieldsets
    new_field = list(field)
    new_field[1][1]['fields'] = ('first_name', 'last_name', 'third_name', 'role', 'email', 'address', 'num', 'birthday',
                                 'floor')
    new_field[2][1]['fields'] = ('is_superuser',)
    fieldsets = new_field
    search_fields = ['email', 'username', 'last_name', 'first_name', 'third_name',
                     'num', 'birthday']
    list_filter = ('role',)


@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'speciality', 'curator']
    list_editable = ['curator']
    list_filter = ('speciality', 'curator')


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['id', 'student']
    list_filter = ('student',)


@admin.register(SubjectToTeacher)
class STTAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'subject', 'group', 'diplom', 'hours']
    list_filter = ('teacher', 'subject', 'group')



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', )
    list_filter = ('group', 'date')


@admin.register(SemesterMarks)
class SemestrMarksAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'student', 'mark')
    list_editable = ['mark', ]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_editable = ['name', ]
    list_display_links = None

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(StudentToGroup)
class STG(admin.ModelAdmin):
    list_filter = ('group',)
    list_display = ['group', 'student', 'zachotka', 'health']
    list_editable = ['group', 'student', 'zachotka', 'health']
    list_display_links = None
