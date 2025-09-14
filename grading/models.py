from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    enrollment_date = models.DateField(auto_now_add=True)
    grade_level = models.CharField(max_length=20)  # e.g., "Grade 7", "Form 2"

    # 🔥 NEW FIELD: link to Class
    current_class = models.ForeignKey(
        'Class',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    parent_guardian_name = models.CharField(max_length=100)
    parent_guardian_phone = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Class(models.Model):
    name = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=20)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=50)   # e.g. "Exam", "Test", "Assignment"
    assessment_name = models.CharField(max_length=100, blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    term = models.CharField(max_length=20)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.max_score and self.score:
            self.percentage = (self.score / self.max_score) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.term})"
