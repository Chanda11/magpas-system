"""
Views for handling user authentication.
"""

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView
from .forms import LoginForm, UserProfileForm
from .models import User
from django.contrib.auth import logout
from django.shortcuts import redirect

class LoginView(FormView):
    """
    Handles user login functionality.
    """
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Authenticate user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    def custom_logout(request):
        logout(request)
        return redirect('login')  # Redirect to login page after logout

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Allows users to view and edit their profile.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'authentication/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Enhanced dashboard for authenticated users.
    """
    template_name = 'authentication/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add actual data from your database
        from grading.models import Student, Subject, Grade
        
        context.update({
            'user': self.request.user,
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_subjects': Subject.objects.count(),
            'total_grades': Grade.objects.count(),
        })
        
        return context