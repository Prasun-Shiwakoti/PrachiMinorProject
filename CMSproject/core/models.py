import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, usertype=None, userId=None):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, usertype=usertype)
        user.set_password(password)  
        user.save(using=self._db)
        return user

def validate_user_type(self,value):
        allowed_user_types = ['student', 'teacher', 'admin']
        if value.lower() not in allowed_user_types:
            raise ValidationError(
                _('%(value)s is not a valid user type. Allowed types are student, teacher, and admin.'),
                params={'value': value},
            )

class CustomUser(AbstractBaseUser):
    #id default hunxa django ma as pk
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    usertype = models.CharField(max_length=20, validators=[validate_user_type])
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

class User(CustomUser):
    class Meta:
        db_table = 'user'

class Faculty(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    credit_hours = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}-{self.faculty}-{self.semester}"

class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=10)
    batch =models.CharField(max_length=10)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    faculty=models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def __str__(self):
        return f"{self.faculty} - {self.name}-{self.semester}"

class Teacher(models.Model):
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    subject =models.ManyToManyField(Subject)

    # delete garyo vaney model k hunxa
    # def delete(self, *args, **kwargs):
    #     # Remove the associated file when the record is deleted
    #     storage, path = self.profile_picture.storage, self.profile_picture.path
    #     super(Teacher, self).delete(*args, **kwargs)
    #     storage.delete(path)

    def __str__(self):
        return f"{self.subject}-{self.name}"

class Admin(models.Model):
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


    def __str__(self):
        return f"{self.id}-{self.role}"

class Marks(models.Model):
    EXAM_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('back', 'Back'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    full_marks = models.DecimalField(max_digits=5, decimal_places=2)
    pass_marks = models.DecimalField(max_digits=5, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    exam_date = models.DateField()
    marks_updated_at = models.DateTimeField(auto_now_add=True)
    marks_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def batch(self):
        return self.student.batch

    def __str__(self):
        return f"{self.subject} - {self.student} - {self.exam_type} Exam - Semester {self.semester}"

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    special = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_name = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in-progress', 'In-Progress'),
            ('completed', 'Completed'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.customer} - {self.status}"
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.order} - {self.total_amount}"

