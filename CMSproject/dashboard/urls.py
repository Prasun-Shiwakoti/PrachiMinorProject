from django.urls import path
from .views import (s_dashboard_view, student_view, teacher_view)

urlpatterns = [
    path('s_dashboard/', s_dashboard_view, name='s_dashboard'),
    path('student/', student_view, name='student_view'),
    path('teacher/', teacher_view, name='teacher_view'),
]
