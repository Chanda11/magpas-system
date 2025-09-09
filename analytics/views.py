from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Avg, Count
from grading.models import Grade, Student, Class

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic statistics
        total_students = Student.objects.filter(is_active=True).count()
        total_grades = Grade.objects.count()
        
        # Performance by subject
        subject_stats = Grade.objects.values('subject__name').annotate(
            avg_score=Avg('percentage'),
            total_grades=Count('id')
        ).order_by('-avg_score')
        
        # Recent grades
        recent_grades = Grade.objects.select_related('student', 'subject').order_by('-date')[:10]
        
        # Grade distribution
        grade_distribution = {
            'A': Grade.objects.filter(percentage__gte=90).count(),
            'B': Grade.objects.filter(percentage__gte=80, percentage__lt=90).count(),
            'C': Grade.objects.filter(percentage__gte=70, percentage__lt=80).count(),
            'D': Grade.objects.filter(percentage__gte=60, percentage__lt=70).count(),
            'F': Grade.objects.filter(percentage__lt=60).count(),
        }
        
        context.update({
            'total_students': total_students,
            'total_grades': total_grades,
            'subject_stats': subject_stats,
            'recent_grades': recent_grades,
            'grade_distribution': grade_distribution,
        })
        
        return context

class StudentPerformanceView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/student_performance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id')
        
        if student_id:
            student = Student.objects.get(student_id=student_id)
            grades = Grade.objects.filter(student=student).select_related('subject')
            
            overall_avg = grades.aggregate(avg=Avg('percentage'))['avg'] or 0
            subject_stats = grades.values('subject__name').annotate(
                avg_score=Avg('percentage'),
                count=Count('id')
            )
            
            context.update({
                'student': student,
                'grades': grades,
                'overall_avg': overall_avg,
                'subject_stats': subject_stats,
            })
        
        return context

class ClassPerformanceView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/class_performance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_id = self.kwargs.get('class_id')
        
        if class_id:
            class_obj = Class.objects.get(id=class_id)
            students = Student.objects.filter(current_class=class_obj, is_active=True)
            
            grades = Grade.objects.filter(student__current_class=class_obj).select_related('student', 'subject')
            
            class_avg = grades.aggregate(avg=Avg('percentage'))['avg'] or 0
            subject_stats = grades.values('subject__name').annotate(
                avg_score=Avg('percentage'),
                count=Count('id')
            )
            
            student_stats = []
            for student in students:
                student_grades = grades.filter(student=student)
                student_avg = student_grades.aggregate(avg=Avg('percentage'))['avg'] or 0
                student_stats.append({
                    'student': student,
                    'average': student_avg,
                    'grade_count': student_grades.count()
                })
            
            student_stats.sort(key=lambda x: x['average'], reverse=True)
            
            context.update({
                'class_obj': class_obj,
                'student_stats': student_stats,
                'class_avg': class_avg,
                'subject_stats': subject_stats,
                'total_students': students.count(),
            })
        
        return context