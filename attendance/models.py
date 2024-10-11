from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username
    
    # cal % de présence
    def attendance_percentage(self):
        total_classes = Attendance.objects.filter(student=self).count()
        if total_classes == 0:
            return 0 
        attended_classes = Attendance.objects.filter(student=self, status='Present').count()
        return (attended_classes / total_classes) * 100

    # éligibilité
    def is_eligible(self):
        return self.attendance_percentage() >= 75

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ])

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"