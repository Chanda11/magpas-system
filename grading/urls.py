from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/add/", views.StudentCreateView.as_view(), name="student_add"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("grades/", views.GradeListView.as_view(), name="grade_list"),
]
