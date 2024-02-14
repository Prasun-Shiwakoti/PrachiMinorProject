from django.http import JsonResponse
from core.models import Admin,Student,Faculty,Marks,Subject
from django.http import Http404
from uuid import UUID
from django.views.decorators.http import require_POST
from examsection.forms.add_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.views import View
from examsection.forms.add_result import UploadResultForm
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import pandas as pd
import json
from django.db import transaction

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


def addresult_view(request, semester, batch, faculty, exam_type):
    user_id = request.session.get('user_id')
    try:
        admin_instance = get_object_or_404(Admin, admin_id=UUID(user_id))
    except Admin.DoesNotExist:
        raise Http404("Admin not found")

    # Pass data to the template
    context = {
        'admin_instance': admin_instance,
        'semester': semester,
        'batch': batch,
        'faculty': faculty,
        'exam_type': exam_type,
    }
    return render(request, 'examsection/add_result.html', context)

def submit_result_file(request):
    print("i was called")
    if request.method == 'POST':
        try:
            with transaction.atomic():
                    print("inside the transaction atomic")
                   
                    data = json.loads(request.body.decode('utf-8')).get('data')
                    semester = json.loads(request.body.decode('utf-8')).get('semester')
                    batch = json.loads(request.body.decode('utf-8')).get('batch')
                    faculty = json.loads(request.body.decode('utf-8')).get('faculty')
                    exam_type = json.loads(request.body.decode('utf-8')).get('exam_type')
                    print("sab values taney js bata")
                    print(f"Received data: {data}")
                    print(f"Semester: {semester}, Batch: {batch}, Faculty: {faculty}, Exam Type: {exam_type}")
                    
                    subjects_in_db = Subject.objects.values_list('name', 'full_marks')
                    subjects_in_file = set(element for element in data[0][2:])  # Assuming the subjects start from the 3rd column
                    print(f"Subjects in file: {subjects_in_file}")
                    missing_subjects = [subject[0] for subject in subjects_in_file if subject[0] not in subjects_in_db]
                    if missing_subjects:
                         raise ValidationError(_('The following subjects do not exist in the database: {}.'.format(', '.join(missing_subjects))))

                    roll_numbers_in_db = Student.objects.values_list('rollNo', 'semester', 'batch', 'faculty', flat=True)
                    roll_numbers_in_file = set(row[0] for row in data[1:])  # Assuming roll numbers are in the 1st column
                    print(f"Roll numbers in file: {roll_numbers_in_file}")
                    if not roll_numbers_in_file.issubset(roll_numbers_in_db):
                        raise ValidationError(_('One or more roll numbers do not exist in the database.'))

                    # Iterate through rows and columns to validate and save marks
                    for row in data[1:]:
                        roll_number, student_semester, student_batch, student_faculty = row[0], row[1], row[2], row[3]
                        student = Student.objects.get(rollNo=roll_number)

                        # Check if student's semester, batch, and faculty match the provided values
                        if student_semester != semester or student_batch != batch or student_faculty != faculty:
                            raise ValidationError(_('Student {} does not match the provided semester, batch, and faculty.'.format(roll_number)))
                        print(f"Processing marks for student {roll_number}, Semester: {student_semester}, Batch: {student_batch}, Faculty: {student_faculty}")
                        for i, subject_name in enumerate(data[0][2:]):
                            subject_full_marks = next(
                                (full_marks,) for name, full_marks in subjects_in_db if name == subject_name
                            )

                            obtained_marks = row[i + 2]  # Assuming marks start from the 3rd column

                            # Validate marks
                            if not (isinstance(obtained_marks, int) and 0 <= obtained_marks <= subject_full_marks):
                                raise ValidationError(_('Invalid marks for subject {} of student {}.'.format(subject_name, roll_number)))
                            print(f"Validated marks for subject {subject_name}: {obtained_marks}")
                            # Save marks to the database
                            Marks.objects.create(
                                subject=subject_name,
                                student=student,
                                full_marks=subject_full_marks,
                                obtained_marks=obtained_marks,
                                faculty=student.faculty,
                                semester=student.semester,
                                exam_type=exam_type,
                                exam_date='2024-02-14',  # You might need to adjust this based on your data
                                marks_updated_by=request.user,  # Assuming you have a user in your request
                            )

                    return JsonResponse({'message': 'Data saved successfully!'}, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': f'Error saving data: {str(e)}'}, status=500)
    return JsonResponse({'the methos is not get'})
       


    

