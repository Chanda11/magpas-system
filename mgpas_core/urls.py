"""
URL configuration for mgpas_core project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# Import views directly
from authentication.views import LoginView, ProfileView, DashboardView
from grading.views import GradeListView, StudentListView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('grading/grades/', GradeListView.as_view(), name='grade_list'),
    path('grading/students/', StudentListView.as_view(), name='student_list'),
   # path('analytics/', include('analytics.urls')),
    #path('reporting/', include('reporting.urls')),
    #path('', include('pwa.urls')),  # PWA URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)