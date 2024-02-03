from django.urls import path
from .views import (s_dashboard_view, t_dashboard_view, student_view, teacher_view)

urlpatterns = [
    path('s_dashboard/<int:user>/', s_dashboard_view, name='s_dashboard'),
    path('t_dashboard/<int:user>/', t_dashboard_view, name='t_dashboard'),
    path('student/<int:user>', student_view, name='student_view'),
    path('teacher/<int:user>', teacher_view, name='teacher_view'),
]
