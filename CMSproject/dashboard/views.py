from django.shortcuts import render
from core.models import Student, Teacher,Marks
from django.http import Http404
from uuid import UUID
from examsection.forms.view_result import FilterForm
from django.http import JsonResponse
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404

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

def handle_viewmy_result_submission(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)

        if form.is_valid():
            filter_metadata = form.get_filter_metadata()
            print("Filter Metadata After Validation:", filter_metadata)
            return JsonResponse({'success': True, 'data': filter_metadata})
        else:
            print("Validation Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def viewmyResult_view(request):
    user_id = request.session.get('user_id')
    student_instance = get_object_or_404(Student, student_id=UUID(user_id))
    
    params = QueryDict(request.GET.urlencode())
    semester = params.get('semester')
    exam_type = params.get('exam_type')

    current_semester = student_instance.semester  # Assuming that the student model has a 'semester' field

    # Check if the queried semester is greater than or equal to the current semester
    if semester is not None and int(semester) >= current_semester:
        semesters = [int(current_semester)]
        query_params = {'student__semester': current_semester, 'exam_type': exam_type}
        results = Marks.objects.filter(**query_params)

        results_by_student = {}
        for result in results:
            student_id = result.student.student_id
            if student_id not in results_by_student:
                results_by_student[student_id] = {'student': result.student, 'subjects': []}
            results_by_student[student_id]['subjects'].append(result)

        # Convert the dictionary values to a list for easier iteration in the template
        organized_results = list(results_by_student.values())

        context = {
            'student_instance': student_instance,
            'distinct_semesters': semesters,
            'exam_type': exam_type,
            'organized_results': organized_results,
        }

        return render(request, 'examsection/view_result.html', context)
    elif semester is None:
        # If semester is None, fetch distinct semester values for the student
        distinct_semesters = Marks.objects.filter(student=student_instance).values_list('student__semester', flat=True).distinct()

        # Fetch and organize results for all semesters from 1 to the current semester
        query_params = {'student__semester__in': range(1, current_semester + 1), 'exam_type': exam_type}
        results = Marks.objects.filter(**query_params)

        results_by_student = {}
        for result in results:
            student_id = result.student.student_id
            if student_id not in results_by_student:
                results_by_student[student_id] = {'student': result.student, 'subjects': []}
            results_by_student[student_id]['subjects'].append(result)

        # Convert the dictionary values to a list for easier iteration in the template
        organized_results = list(results_by_student.values())

        context = {
            'student_instance': student_instance,
            'exam_type': exam_type,
            'organized_results': organized_results,
            'distinct_semesters': distinct_semesters,
        }

        return render(request, 'examsection/view_result.html', context)
    else:
        # Display an error message
        error_message = "Invalid semester. Please enter a semester greater than or equal to the current semester."
        context = {
            'student_instance': student_instance,
            'error_message': error_message,
        }

        return JsonResponse (context)


