from django.urls import path
from .views.exam import examsection_view
from .views.add_result import handle_add_result_submission, addresult_view , upload_result_file
from .views.view_result import handle_view_result_submission, viewresult_view


urlpatterns =[
    path('handle_add_result_submission/', handle_add_result_submission,name='handle_add_result_submission'),
    path('handle_view_result_submission/', handle_view_result_submission,name='handle_view_result_submission'),
    #path('handle_student_analysis_submission/', handle_filter_submission,name='handle_student_analysis_submission'),
    path('exam/', examsection_view, name='examsection_view'),
    path('addresult/<int:semester>/<int:batch>/<str:faculty>/<str:exam_type>/', addresult_view, name='addresult_view'),
    path('viewresult/', viewresult_view, name='viewresult_view'),
    path('addresultfile/', upload_result_file.as_view(), name='upload_result_file'),
]