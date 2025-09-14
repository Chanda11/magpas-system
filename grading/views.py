from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from .models import Student


class StudentListView(ListView):
    model = Student
    template_name = "grading/students.html"
    context_object_name = "students"
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.filter(is_active=True)
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search_query)
                | models.Q(last_name__icontains=search_query)
                | models.Q(student_id__icontains=search_query)
            )
        return queryset


class StudentDetailView(DetailView):
    model = Student
    template_name = "grading/student_detail.html"
    context_object_name = "student"


class StudentCreateView(CreateView):
    model = Student
    template_name = "grading/student_form.html"
    fields = "__all__"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        messages.success(self.request, "Student created successfully!")
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    model = Student
    template_name = "grading/student_form.html"
    fields = "__all__"

    def get_success_url(self):
        messages.success(self.request, "Student updated successfully!")
        return reverse_lazy("student_detail", kwargs={"pk": self.object.pk})


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "grading/student_confirm_delete.html"
    success_url = reverse_lazy("student_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Student deleted successfully!")
        return super().delete(request, *args, **kwargs)

from .models import Grade

class GradeListView(ListView):
    model = Grade
    template_name = "grading/grades.html"
    context_object_name = "grades"
    paginate_by = 20

    def get_queryset(self):
        queryset = Grade.objects.all().select_related("student", "subject", "academic_year")
        # Optional search filter
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                models.Q(student__first_name__icontains=search_query)
                | models.Q(student__last_name__icontains=search_query)
                | models.Q(subject__name__icontains=search_query)
                | models.Q(assessment_name__icontains=search_query)
            )
        return queryset
