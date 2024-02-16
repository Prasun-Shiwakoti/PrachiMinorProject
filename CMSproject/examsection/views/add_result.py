from django.http import JsonResponse
from core.models import Student,Marks,Subject
from django.views.decorators.http import require_POST
from examsection.forms.add_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from examsection.forms.add_result import UploadResultForm
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import pandas as pd
from datetime import datetime, date
from decimal import Decimal
import json
from django.db import transaction
from django.contrib.auth.decorators import login_required

@csrf_protect
def handle_add_result_submission(request):
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

@login_required
def addresult_view(request, semester, batch, faculty, exam_type):
    user = request.user  # Django's authenticated user
    if user.usertype == 'admin':
        admin_instance = user.admin
    print(semester)
    print(faculty)
    print(batch)
    print(exam_type)
    existing_marks = Marks.objects.filter(
        student__semester=semester,
        student__faculty__name=faculty,
        student__batch=batch,
        exam_type=exam_type
    )

    # If there are existing entries, return a JSON response
    if existing_marks.exists():
        return render(request, 'examsection/exam.html', {'admin_instance': admin_instance})
    
    context = {
        'admin_instance': admin_instance,
        'semester': semester,
        'batch': batch,
        'faculty': faculty,
        'exam_type': exam_type,
    }
    return render(request, 'examsection/add_result.html', context)

@login_required
def submit_result_file(request):
    user = request.user  # Django's authenticated user
    if user.usertype == 'admin':
        admin_instance = user.admin
    if request.method == 'POST':
        try:
            with transaction.atomic():
                    data = json.loads(request.body.decode('utf-8')).get('data')
                    semester = int(json.loads(request.body.decode('utf-8')).get('semester'))
                    batch = json.loads(request.body.decode('utf-8')).get('batch')
                    faculty = json.loads(request.body.decode('utf-8')).get('faculty')
                    exam_type = json.loads(request.body.decode('utf-8')).get('exam_type')
                    
                    subjects_in_db = Subject.objects.values_list('name', 'full_marks')
                    subjects_in_db_names = [subject[0].lower() for subject in subjects_in_db]
                    subjects_in_file = set(element.lower() for element in data[0][2:]) 

                    missing_subjects = [subject for subject in subjects_in_file if subject not in subjects_in_db_names]

                    if missing_subjects:
                        raise ValidationError(_('The following subjects do not exist in the database: {}.'.format(', '.join(missing_subjects))))


                    students_in_db = Student.objects.values_list('rollNo', 'semester', 'batch', 'faculty')
                    roll_numbers_in_db_rollNo = [str(rollNo[0]) for rollNo in students_in_db] 
                    roll_numbers_in_file = [str(row[0]) for row in data[1:]]  
                    roll_numbers_in_file_sorted = list(roll_numbers_in_file)

                    roll_numbers_in_file_sorted.sort()
                    roll_numbers_in_db_rollNo.sort()

                    if roll_numbers_in_file_sorted != roll_numbers_in_db_rollNo:
                        missing_roll_numbers = [roll_number for roll_number in roll_numbers_in_file if roll_number not in roll_numbers_in_db_rollNo]
                        raise ValidationError(_('One or more roll numbers do not exist in the database. Missing roll numbers: {}.'.format(', '.join(missing_roll_numbers))))
                    for roll_number in roll_numbers_in_file:
                        student = Student.objects.get(rollNo=roll_number)

                        print('pass vayexa loose equality haha Check for strict inequality')
                        if student.semester != semester or student.batch != batch or str(student.faculty.name) != faculty:
                            raise ValidationError(_('Student {} does not match the provided semester, batch, and faculty.'.format(roll_number)))
                        for i, subject_name in enumerate(data[0][2:]):
                                subject_full_marks = next(
                                    (full_marks,) for name, full_marks in subjects_in_db if name.lower() == subject_name.lower()
                                )
                                
                                subjects_instance = get_object_or_404(Subject, name = subject_name.lower())
                                subject_full_marks = subject_full_marks[0]
                                obtained_marks = Decimal(data[roll_numbers_in_file.index(roll_number) + 1][i + 2]) 
                                
                                if not (isinstance(obtained_marks, Decimal) and 0 <= obtained_marks <= subject_full_marks):
                                    raise ValidationError(_('Invalid marks {} for subject {} of student {}. Marks should be an integer between 0 and {}.'.format(obtained_marks, subject_name, roll_number, subject_full_marks)))
                    
                                Marks.objects.create(
                                    subject=subjects_instance,
                                    student=student,
                                    obtained_marks=obtained_marks,
                                    exam_type=exam_type,
                                    exam_date=date.today(),
                                    marks_updated_by=admin_instance,  
                                )
            return JsonResponse({'message': 'Data saved successfully!'}, status=200)    
        except ValidationError as ve:
            return JsonResponse({'error': f'Validation error: {str(ve)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error saving data: {str(e)}'}, status=500)
    return JsonResponse({'the methos is not get'})
       


    

