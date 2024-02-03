from django.contrib import admin
from .models import Student, Teacher, Admin, CustomUser, Faculty, Subject, Marks

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Subject)
admin.site.register(Marks)
