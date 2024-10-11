from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('login/', views.user_login, name='login'), 
    path('', views.home, name='home'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'), 
    path('attendance_success/', views.attendance_success, name='attendance_success'),  
    path('attendance_report/', views.attendance_report, name='attendance_report'), 
    path('student_report/<str:student_id>/', views.student_attendance_report, name='student_report'), # si tu veux tager par un id qui a des lettres <str:student_id>
    path('class_report/', views.class_attendance_report, name='class_report'), 
    path('search/', views.search_students, name='search_students'), 
]
