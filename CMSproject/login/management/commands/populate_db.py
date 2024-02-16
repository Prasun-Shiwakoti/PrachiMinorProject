from django.core.management.base import BaseCommand
from django.core.files import File
import os
from django.contrib.auth import get_user_model
from core.models import CustomUser, Student, Teacher, Admin, Faculty, MenuItem, Order,Subject,Facultysubject

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        # Create Faculty
        computer_faculty = Faculty.objects.create(name='Computer')
        civil_faculty = Faculty.objects.create(name='Civil')
        subject_applied_mechanics = Subject.objects.create(name='Applied Mechanics', credit_hours=3, full_marks=100, pass_marks=40)
        subject_basic_electronics = Subject.objects.create(name='Basic Electronics', credit_hours=3, full_marks=100, pass_marks=40)
        subject_maths_computer = Subject.objects.create(name='Mathematics', credit_hours=3, full_marks=100, pass_marks=40)

        # Create Facultysubject entry for Computer faculty Semester 6
        facultysubject_computer_semester6 = Facultysubject.objects.create(faculty=computer_faculty, semester=6)
        facultysubject_computer_semester6.subject.add(subject_applied_mechanics, subject_basic_electronics, subject_maths_computer)

        # Create subjects for Civil faculty in Semester 6
        subject_soil_mechanics = Subject.objects.create(name='Soil Mechanics', credit_hours=3, full_marks=100, pass_marks=40)
        subject_hydrology = Subject.objects.create(name='Hydrology', credit_hours=3, full_marks=100, pass_marks=40)
        subject_maths_civil = Subject.objects.create(name='Mathematics', credit_hours=3, full_marks=100, pass_marks=40)

        # Create Facultysubject entry for Civil faculty Semester 6
        facultysubject_civil_semester6 = Facultysubject.objects.create(faculty=civil_faculty, semester=6)
        facultysubject_civil_semester6.subject.add(subject_soil_mechanics, subject_hydrology, subject_maths_civil)

        student_user2 = CustomUser.objects.create_user(email='student2@example.com', usertype='student')
        student2 = Student.objects.create(user=student_user2, name='Student 2', rollNo='077bct040', batch='2077', semester='6', faculty=computer_faculty)
        student_user2.set_password('12345')
        student_user2.save()

        student_user3 = CustomUser.objects.create_user(email='student3@example.com', usertype='student')
        student3 = Student.objects.create(user=student_user3, name='Student 3', rollNo='077bct041', batch='2077', semester='6', faculty=computer_faculty)
        student_user3.set_password('12345')
        student_user3.save()

        student_user4 = CustomUser.objects.create_user(email='student4@example.com', usertype='student')
        student4 = Student.objects.create(user=student_user4, name='Student 4', rollNo='077bct042', batch='2077', semester='6', faculty=computer_faculty)
        student_user4.set_password('12345')
        student_user4.save()

        # Create more students for the Civil faculty
        student_user5 = CustomUser.objects.create_user(email='student5@example.com', usertype='student')
        student5 = Student.objects.create(user=student_user5, name='Student 5', rollNo='077bce043', batch='2077', semester='6', faculty=civil_faculty)
        student_user5.set_password('12345')
        student_user5.save()

        student_user6 = CustomUser.objects.create_user(email='student6@example.com', usertype='student')
        student6 = Student.objects.create(user=student_user6, name='Student 6', rollNo='077bce044', batch='2077', semester='6', faculty=civil_faculty)
        student_user6.set_password('12345')
        student_user6.save()

        student_user7 = CustomUser.objects.create_user(email='student7@example.com', usertype='student')
        student7 = Student.objects.create(user=student_user7, name='Student 7', rollNo='077bce045', batch='2077', semester='6', faculty=civil_faculty)
        student_user7.set_password('12345')
        student_user7.save()
        # Create Students
        student_user1 = CustomUser.objects.create_user(email='student1@example.com', usertype='student')
        student1 = Student.objects.create(user=student_user1, name='Student 1', rollNo='077bct039', batch='2077', semester='6', faculty=computer_faculty)
        student_user1.set_password('12345')
        student_user1.save()
        self.add_profile_picture(student1, 'media/student1.jpg')

        # Create Teachers
        teacher_user1 = CustomUser.objects.create_user(email='teacher1@example.com', usertype='teacher')
        teacher1 = Teacher.objects.create(user=teacher_user1, name='Teacher 1')
        teacher_user1.set_password('67890')
        teacher_user1.save()
        self.add_profile_picture(teacher1, 'media/teacher1.jpg')

        # Create Admins
        admin_user1 = CustomUser.objects.create_user(email='admin1@example.com', usertype='admin')
        admin_user1.set_password('exam12345')
        admin_user1.save()
        admin1 = Admin.objects.create(user=admin_user1, name='Admin 1', role='exam')
        self.add_profile_picture(admin1, 'media/examadmin1.jpg')

        admin_user2 = CustomUser.objects.create_user(email='admin2@example.com', usertype='admin')
        admin2 = Admin.objects.create(user=admin_user2, name='Admin 2', role='staff')
        admin_user2.set_password('staff12345')
        admin_user2.save()
        self.add_profile_picture(admin2, 'media/staffadmin1.webp')

        # Create Menu Items
        menu_item1 = MenuItem.objects.create(name='Burger', price=200, description='Delicious burger')
        menu_item2 = MenuItem.objects.create(name='pastry', price=60, description='juicy pastry')
        self.add_image(menu_item1, 'media/burger.webp')        
        self.add_image(menu_item2, 'media/cake.webp')  

        # Fetch the created custom users and menu items
        student_user1 = get_user_model().objects.get(email='student1@example.com')
        teacher_user1 = get_user_model().objects.get(email='teacher1@example.com')
        menu_item1 = MenuItem.objects.get(name='Burger')
        menu_item2 = MenuItem.objects.get(name='pastry')

        # Create orders for students
        order_student1_burger = Order.objects.create(
            customer=student_user1,
            order_name=menu_item1,
            quantity=2,  # Set the desired quantity
            status='in-progress'
        )

        order_student1_pastry = Order.objects.create(
            customer=student_user1,
            order_name=menu_item2,
            quantity=1,  # Set the desired quantity
            status='completed'
        )

        # Create orders for teachers
        order_teacher1_burger = Order.objects.create(
            customer=teacher_user1,
            order_name=menu_item1,
            quantity=3,  # Set the desired quantity
            status='in-progress'
        )

        order_teacher1_pastry = Order.objects.create(
            customer=teacher_user1,
            order_name=menu_item2,
            quantity=1,  # Set the desired quantity
            status='completed'
        )

    def add_image(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.image.save(os.path.basename(file_path), File(f))

    def add_profile_picture(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.profile_picture.save(os.path.basename(file_path), File(f))
