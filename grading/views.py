from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Grade, Student

class GradeListView(LoginRequiredMixin, ListView):
    """View to list grades"""
    model = Grade
    template_name = 'grading/grade_list.html'
    context_object_name = 'grades'
    
    def get_queryset(self):
        return Grade.objects.all().select_related('student', 'subject').order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_grades'] = Grade.objects.count()
        return context

class StudentListView(LoginRequiredMixin, ListView):
    """View to list students"""
    model = Student
    template_name = 'grading/student_list.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        return Student.objects.all().select_related('current_class').order_by('last_name', 'first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        return context