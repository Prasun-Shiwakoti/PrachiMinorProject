#forms.py
from django import forms 
from core.models import Faculty, Marks, Subject

class FilterForm(forms.form):
    faculty_choices=[
        ('Computer', 'computer'),
        ('Civil', 'civil'),
        ('Architecture', 'architecture'),
        ('Electrical', 'electrical'),
        ('Electronics', 'electronics'),
    ]
    semester_choices=[(str(i), str(i)) for i in range(1,9)]
    exam_type_choices = [('Regular', 'regular'), ('Back', 'back')]

    faculty=forms.ChoiceField(choices=faculty_choices, required=False)
    semester=forms.ChoiceField(choices=semester_choices, required=False)
    exam_type=forms.ChoiceField(exam_type_choices, required=False)
    batch_number=forms.IntegerField(min_value=1998, required=False)

    def apply_filters(self):
        faculty=self.cleaned_data['faculty']
        semester=self.cleaned_data['semeter']
        exam_type=self.cleaned_data['exam_type']
        batch_number=self.cleaned_data['batch_number']

        filtered_marks=Marks.objects.fiter(
            faculty=faculty,
            semester=semester,
            exam_type=exam_type,
            batch_number=batch_number,
        )

        return filtered_marks