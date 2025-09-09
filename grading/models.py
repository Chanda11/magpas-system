from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class AcademicYear(models.Model):
    """Represents an academic year (e.g., 2023-2024)"""
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    """Represents a subject taught at the school"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Class(models.Model):
    """Represents a class/grade level (e.g., Grade 7A)"""
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20)  # e.g., "Grade 7", "Grade 8"
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'TEACHER'})
    
    class Meta:
        unique_together = ['name', 'academic_year']
        ordering = ['grade_level', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class Student(models.Model):
    """Represents a student"""
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['current_class', 'last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Grade(models.Model):
    """Represents a student's grade for an assessment"""
    ASSESSMENT_TYPES = (
        ('EXAM', 'Exam'),
        ('QUIZ', 'Quiz'),
        ('ASSIGNMENT', 'Assignment'),
        ('PROJECT', 'Project'),
        ('PARTICIPATION', 'Class Participation'),
    )
    
    TERM_CHOICES = (
        ('TERM1', 'Term 1'),
        ('TERM2', 'Term 2'),
        ('TERM3', 'Term 3'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    assessment_name = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100, validators=[MinValueValidator(1)])
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField()
    entered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'assessment_name', 'term', 'academic_year']
        ordering = ['-date', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.assessment_name} ({self.percentage}%)"
    
    def save(self, *args, **kwargs):
        # Calculate percentage before saving
        if self.score and self.max_score:
            self.percentage = (self.score / self.max_score) * 100
        super().save(*args, **kwargs)
    
    def get_grade_letter(self):
        """Convert percentage to letter grade"""
        if self.percentage >= 90:
            return 'A'
        elif self.percentage >= 80:
            return 'B'
        elif self.percentage >= 70:
            return 'C'
        elif self.percentage >= 60:
            return 'D'
        else:
            return 'F'