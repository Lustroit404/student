from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import student

@admin.register(student)
class studentAdmin(admin.ModelAdmin):
    list_display = ['student_name','courses','scores','fail_count','latest_retake_score','retake_classroom','course_time']