from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from .models import Attendance, Student

from .models import Student
from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def mark_attendance(request):
    if request.method == 'POST':
        for student_id in request.POST:
            if student_id.startswith('student_'):
                student = Student.objects.get(id=student_id.split('_')[1])
                status = request.POST.get(student_id)
                Attendance.objects.create(student=student, status=status)
        return redirect('attendance_success')
    
    students = Student.objects.all()
    return render(request, 'attendance/mark_attendance.html', {'students': students})

def attendance_success(request):
    return render(request, 'attendance/attendance_success.html')

def home(request):
    return render(request, 'attendance/home.html')

def attendance_report(request):
    students = Student.objects.all()
    return render(request, 'attendance/attendance_report.html', {'students': students})

def student_attendance_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)# ne foctionne pas
    attendance_records = Attendance.objects.filter(student=student)
    total_classes = attendance_records.count()
    attended_classes = attendance_records.filter(status='Present').count()
    attendance_percentage = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
    return render(request, 'attendance/student_report.html', {
        'student': student,
        'attendance_records': attendance_records,
        'total_classes': total_classes,
        'attended_classes': attended_classes,
        'attendance_percentage': attendance_percentage,
    })

def class_attendance_report(request):
    students = Student.objects.all()
    class_attendance = []

    for student in students:
        total_classes = Attendance.objects.filter(student=student).count()
        attended_classes = Attendance.objects.filter(student=student, status='Present').count()
        attendance_percentage = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
        class_attendance.append({
            'student': student,
            'total_classes': total_classes,
            'attended_classes': attended_classes,
            'attendance_percentage': attendance_percentage,
        })

    return render(request, 'attendance/class_report.html', {'class_attendance': class_attendance})

def search_students(request):
    form = SearchForm(request.GET)
    students = Student.objects.all() 
    attendance_records = Attendance.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        date = form.cleaned_data.get('date')

 # Rechercher par nom/ID étudiant
        if query:
            students = students.filter(
                Q(user__username__icontains=query) | Q(student_id__icontains=query)
            )

# Filtrer par date d'assiduité
        if date:
            attendance_records = attendance_records.filter(date=date)

    return render(request, 'attendance/search_results.html', {
        'form': form,
        'students': students,
        'attendance_records': attendance_records,
    })