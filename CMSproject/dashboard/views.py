from django.shortcuts import render
from core.models import Student, Teacher
from django.http import Http404

def s_dashboard_view(request, user):
    try:
        student_instance= Student.objects.get(id=user)
        context={'student_instance':student_instance}
        return render(request, 'dashboard/s_dashboard.html', context)
    except Student.DoesNotExist:
        raise Http404 ("student not found") 
    
def t_dashboard_view(request, user):
    try:
        teacher_instance=Teacher.objects.get(id=user)
        context={'teacher_instance':teacher_instance}
        return render(request, 'dashboard/t_dashboard.html',context)
    except Teacher.DoesNotExist:
        raise Http404 ("teacher not found")
     
def student_view(request,user):
    try:
        student_instance= Student.objects.get(id=user)
        context={'student_instance':student_instance}
        return render(request, 'dashboard/student.html', context)
    except Student.DoesNotExist:
        raise Http404 ("student not found") 
    
def teacher_view(request, user):
    try:
        teacher_instance=Teacher.objects.get(id=user)
        context={'teacher_instance':teacher_instance}
        return render(request, 'dashboard/teacher.html',context)
    except Teacher.DoesNotExist:
        raise Http404 ("teacher not found") 