"""
URL configuration for mgpas_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# Import views directly
from authentication.views import LoginView, ProfileView, DashboardView
from grading.views import GradeListView, StudentListView

# Import your custom logout view
from . import views  # Add this import

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('grading/grades/', GradeListView.as_view(), name='grade_list'),
    path('grading/students/', StudentListView.as_view(), name='student_list'),

    # Add these to your urlpatterns list
    path('attendance/', TemplateView.as_view(template_name='coming_soon.html'), name='attendance'),
    path('classes/', TemplateView.as_view(template_name='coming_soon.html'), name='classes'),
    path('exams/', TemplateView.as_view(template_name='coming_soon.html'), name='exams'),
    path('timetable/', TemplateView.as_view(template_name='coming_soon.html'), name='timetable'),
    path('admin/logout/', views.custom_logout, name='logout'),
       # Students
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # Grades
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    # Use the simple function view for logout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)