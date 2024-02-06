from django.urls import path
from .views import (s_dashboard_view, student_view, teacher_view)

urlpatterns = [
    path('s_dashboard/<uuid:user>/', s_dashboard_view, name='s_dashboard'),
    path('student/<uuid:user>', student_view, name='student_view'),
    path('teacher/<uuid:user>', teacher_view, name='teacher_view'),
]
