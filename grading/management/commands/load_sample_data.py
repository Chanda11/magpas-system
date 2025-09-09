from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from grading.models import AcademicYear, Subject, Class, Student, Grade
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Load sample data for testing the grading system'
    
    def handle(self, *args, **options):
        # Create academic year
        current_year, created = AcademicYear.objects.get_or_create(
            name="2023-2024",
            defaults={
                'start_date': date(2023, 9, 1),
                'end_date': date(2024, 6, 30),
                'is_current': True
            }
        )
        
        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH'},
            {'name': 'English Language', 'code': 'ENG'},
            {'name': 'Science', 'code': 'SCI'},
            {'name': 'Social Studies', 'code': 'SOC'},
            {'name': 'Local Language', 'code': 'LOC'},
        ]
        
        subjects = {}
        for data in subjects_data:
            subject, created = Subject.objects.get_or_create(**data)
            subjects[data['code']] = subject
        
        # Create a teacher if not exists
        teacher, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'first_name': 'John',
                'last_name': 'Teacher',
                'email': 'teacher@musenga.edu.zm',
                'role': 'TEACHER'
            }
        )
        if created:
            teacher.set_password('password123')
            teacher.save()
        
        # Create a class
        grade7a, created = Class.objects.get_or_create(
            name='Grade 7A',
            academic_year=current_year,
            defaults={
                'grade_level': 'Grade 7',
                'teacher': teacher
            }
        )
        
        # Create some students
        students_data = [
            {'student_id': 'ST001', 'first_name': 'Alice', 'last_name': 'Banda', 'date_of_birth': date(2010, 5, 15)},
            {'student_id': 'ST002', 'first_name': 'Bob', 'last_name': 'Phiri', 'date_of_birth': date(2010, 8, 22)},
            {'student_id': 'ST003', 'first_name': 'Carol', 'last_name': 'Mwale', 'date_of_birth': date(2011, 2, 10)},
            {'student_id': 'ST004', 'first_name': 'David', 'last_name': 'Tembo', 'date_of_birth': date(2010, 11, 5)},
        ]
        
        students = {}
        for data in students_data:
            student, created = Student.objects.get_or_create(
                student_id=data['student_id'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'date_of_birth': data['date_of_birth'],
                    'enrollment_date': date(2023, 9, 1),
                    'current_class': grade7a,
                    'is_active': True
                }
            )
            students[data['student_id']] = student
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )