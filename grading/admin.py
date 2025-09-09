from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AcademicYear, Subject, Class, Student, Grade

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_editable = ('is_current',)
    list_filter = ('is_current',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'academic_year', 'teacher')
    list_filter = ('academic_year', 'grade_level')
    search_fields = ('name', 'grade_level')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'current_class', 'is_active')
    list_filter = ('current_class', 'is_active')
    search_fields = ('student_id', 'first_name', 'last_name')
    list_editable = ('is_active',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'assessment_type', 'score', 'max_score', 'percentage', 'term', 'date')
    list_filter = ('subject', 'assessment_type', 'term', 'academic_year', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'assessment_name')
    readonly_fields = ('percentage',)