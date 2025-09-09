from django.urls import path
from .views import GradeListView, StudentListView

app_name = 'grading'

urlpatterns = [
    path('grades/', GradeListView.as_view(), name='grade_list'),
    path('students/', StudentListView.as_view(), name='student_list'),
]