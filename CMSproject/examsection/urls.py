from django.urls import path
from .views.exam import examsection_view
from .views.add_result import handle_filter_submission, addresult_view , upload_result_file

urlpatterns =[
    path('handle_filter_submission/', handle_filter_submission,name='handle_filter_submission'),
    path('exam/', examsection_view, name='examsection_view'),
    path('addresult/<int:semester>/<int:batch>/<str:faculty>/<str:exam_type>/', addresult_view, name='addresult_view'),
    path('addresultfile/', upload_result_file.as_view(), name='upload_result_file'),
]