from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Avg, Count, Q
from grading.models import Grade, Student, Class, Subject
import csv
from datetime import datetime

class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reporting/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        
        context.update({
            'classes': classes,
            'subjects': subjects,
        })
        return context

class StudentReportView(LoginRequiredMixin, View):
    def get(self, request, student_id):
        student = Student.objects.get(student_id=student_id)
        grades = Grade.objects.filter(student=student).select_related('subject')
        
        overall_avg = grades.aggregate(avg=Avg('percentage'))['avg'] or 0
        subject_stats = grades.values('subject__name').annotate(
            avg_score=Avg('percentage'),
            count=Count('id')
        )
        
        html_content = render_to_string('reporting/student_report.html', {
            'student': student,
            'grades': grades,
            'overall_avg': overall_avg,
            'subject_stats': subject_stats,
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="student_report_{student_id}.html"'
        return response

class ClassReportView(LoginRequiredMixin, View):
    def get(self, request, class_id):
        class_obj = Class.objects.get(id=class_id)
        students = Student.objects.filter(current_class=class_obj, is_active=True)
        grades = Grade.objects.filter(student__current_class=class_obj)
        
        class_avg = grades.aggregate(avg=Avg('percentage'))['avg'] or 0
        subject_stats = grades.values('subject__name').annotate(
            avg_score=Avg('percentage'),
            count=Count('id')
        )
        
        html_content = render_to_string('reporting/class_report.html', {
            'class_obj': class_obj,
            'students': students,
            'class_avg': class_avg,
            'subject_stats': subject_stats,
            'total_students': students.count(),
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="class_report_{class_obj.name}.html"'
        return response

class CSVExportView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mgpas_data_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Student Name', 'Class', 'Subject', 'Assessment', 'Score', 'Percentage', 'Grade', 'Term', 'Date'])
        
        grades = Grade.objects.select_related('student', 'subject', 'student__current_class')
        for grade in grades:
            writer.writerow([
                grade.student.student_id,
                f"{grade.student.first_name} {grade.student.last_name}",
                grade.student.current_class.name if grade.student.current_class else 'N/A',
                grade.subject.name,
                grade.assessment_name,
                f"{grade.score}/{grade.max_score}",
                f"{grade.percentage}%",
                grade.get_grade_letter(),
                grade.get_term_display(),
                grade.date.strftime("%Y-%m-%d")
            ])
        
        return response