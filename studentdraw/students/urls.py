from django.contrib import admin
from django.urls import path

from . import views
urlpatterns=[
    path("student_list/",views.student_list,name='student_list'),
    path('add_or_update_student',views.add_or_update_student,name='add_or_update_student'),
    #path('students/',views.StudentListCreateView.as_view(),name='student-list-create'),
    path("students/<int:id>/",views.StudentDetailView.as_view(),name='student-detail'),
    path('students/',views.StudentPostView.as_view(),name='student-post')
]