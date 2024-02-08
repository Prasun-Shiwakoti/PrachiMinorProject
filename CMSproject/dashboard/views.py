from django.shortcuts import render
from core.models import Student, Teacher
from django.http import Http404
from uuid import UUID

def s_dashboard_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            student_instance = Student.objects.get(student_id=UUID(user_id))
            context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student'}
            return render(request, 'dashboard/s_dashboard.html', context)
        except Student.DoesNotExist:
            try:
                # If Student is not found, attempt to get a Teacher instance
                teacher_instance = Teacher.objects.get(teacher_id=UUID(user_id))
                context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher'}
                return render(request, 'dashboard/s_dashboard.html', context)
            except Teacher.DoesNotExist:
                raise Http404("User not found")
    else:
        raise Http404("User ID not found in session")

     
def student_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            student_instance = Student.objects.get(student_id=UUID(user_id))
            context = {'student_instance': student_instance}
            return render(request, 'dashboard/student.html', context)
        except Student.DoesNotExist:
            raise Http404("User not found")
    
def teacher_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            teacher_instance=Teacher.objects.get(teacher_id=UUID(user_id))
            context={'teacher_instance':teacher_instance}
            return render(request, 'dashboard/teacher.html',context)
        except Teacher.DoesNotExist:
            raise Http404 ("teacher not found") 