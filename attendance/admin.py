from django.contrib import admin

# Register your models here.
from .models import Student, Attendance

# Enregistrer modèles ds l'admin
admin.site.register(Student)
admin.site.register(Attendance)