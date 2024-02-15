from django.shortcuts import render, get_object_or_404
from core.models import Admin
from uuid import UUID
from django.http import Http404
from examsection.forms.view_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.http import QueryDict
from core.models import Faculty, Subject, Facultysubject

def examsection_view(request):
    user_id = request.session.get('user_id')
    try:
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
        return render(request, 'examsection/exam.html', {'admin_instance': admin_instance})
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    
@csrf_protect
def handle_course_Info_submisssion(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        print(request.POST)

        if form.is_valid():
            filter_metadata = form.get_filter_metadata()
            print("Filter Metadata After Validation:", filter_metadata)
            return JsonResponse({'success': True, 'data': filter_metadata})
        else:
            print("Validation Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def courseInfo_view(request):
    user_id = request.session.get('user_id')
    try:
        admin_instance = get_object_or_404(Admin, admin_id=UUID(user_id))
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    
    params = QueryDict(request.GET.urlencode())
    semester = params.get('semester')
    faculty = params.get('faculty')
    print(f'Semester: {semester}, Faculty: {faculty}')

    # Build the dynamic query based on the selected filters
    query_params = {}
    if semester is not None:
        query_params['semester'] = semester
    if faculty is not None:
        query_params['faculty__name'] = faculty

    results = Facultysubject.objects.filter(**query_params)
    for result in results:
        print(f'Faculty: {result.faculty.name}, Semester: {result.semester}, Subjects: {[subject.name for subject in result.subject.all()]}')
    
    if faculty == 'Architecture':
        semester_range = range(1, 11)
    else:
        semester_range = range(1, 9)

    context = {
        'admin_instance': admin_instance,
        'semester': semester,
        'faculty': faculty,
        'results': results,
        'semester_range':semester_range,
    }

    return render(request, 'examsection/courseInfo.html', context)