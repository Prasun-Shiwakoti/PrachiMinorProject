#forms.py
from django import forms 
import pandas as pd

class FilterForm(forms.Form):
    faculty_choices = [
        ('Computer', 'computer'),
        ('Civil', 'civil'),
        ('Architecture', 'architecture'),
        ('Electrical', 'electrical'),
        ('Electronics', 'electronics'),
    ]
    semester_choices = [(str(i), str(i)) for i in range(1, 9)]
    exam_type_choices = [('Regular', 'regular'), ('Back', 'back')]

    faculty = forms.ChoiceField(choices=faculty_choices, required=True)
    semester = forms.ChoiceField(choices=semester_choices, required=True)
    exam_type = forms.ChoiceField(choices=exam_type_choices, required=False)
    batch_number = forms.IntegerField(min_value=1998, required=True)

    def get_filter_metadata(self):
        # Return a dictionary containing the import metadata
        return {
            'faculty': self.cleaned_data['faculty'],
            'semester': self.cleaned_data['semester'],
            'exam_type': self.cleaned_data['exam_type'],
            'batch_number': self.cleaned_data['batch_number'],
        }

class UploadResultForm(forms.Form):
    file_input = forms.FileField(
        label='Select a file',
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx, .xls, .csv'}),
    )

    def clean_file_input(self):
        file = self.cleaned_data.get('file_input')
        if file:
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                try:
                    df = pd.read_excel(file)
                except pd.errors.ParserError:
                    raise forms.ValidationError("Error reading the Excel file. Please provide a valid Excel file.")

            elif file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(file)
                except pd.errors.ParserError:
                    raise forms.ValidationError("Error reading the CSV file. Please provide a valid CSV file.")

            else:
                raise forms.ValidationError("Invalid file type. Please upload an Excel (.xlsx, .xls) or CSV file.")

            required_columns = ['Roll No.', 'Student Name', 'Subject', 'Marks']
            for column in required_columns:
                if column not in df.columns:
                    raise forms.ValidationError(f"Column '{column}' is missing. Please provide valid columns.")

            for roll_no in df['Roll No.']:
                if not self.is_valid_roll_no(roll_no):
                    raise forms.ValidationError(f"Invalid 'Roll No.': {roll_no}")

            for index, row in df.iterrows():
                subject = row['Subject']
                marks = row['Marks']

                # Check if 'Marks' is a positive integer
                if not isinstance(marks, int) or marks < 0:
                    raise forms.ValidationError(f"Invalid marks for subject '{subject}': {marks}")

                # Add your custom validation logic for subject marks and full marks
                if not self.is_valid_subject_marks(subject, marks):
                    raise forms.ValidationError(f"Invalid marks for subject '{subject}': {marks}")

        return file

    def is_valid_roll_no(self, roll_no):
        # Add your custom validation logic for roll numbers
        return True

    def is_valid_subject_marks(self, subject, marks):
        # Add your custom validation logic for subject marks and full marks
        return True

        
