from django.urls import path
from . import views

app_name = 'analytics'  # This line is CRITICAL

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('student/<str:student_id>/', views.StudentPerformanceView.as_view(), name='student_performance'),
    path('class/<int:class_id>/', views.ClassPerformanceView.as_view(), name='class_performance'),
]