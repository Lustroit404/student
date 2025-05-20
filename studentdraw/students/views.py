from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import studentSerializer
from .models import student
import json

def student_list(request):
    profiles=student.objects.all()
    data=[]
    for profile in profiles:
        data.append({
            "student_name":profile.student_name,
            "courses":profile.courses,
            "fail_count":profile.fail_count,
            "retake_count":profile.retake_count,
            "latest_retake_score":profile.latest_retake_score,
            "retake_classroom":profile.retake_classroom,
            "course_time":profile.course_time,
            "warning_courses":profile.course_time,
            "total_courses":len(profile.courses),
            "total_fail_courses":profile.fail_count
        })
    return JsonResponse(data,safe=False)

def add_or_update_student(request):
    if request.method == 'POST':
        student_name=request.POST.get("student_name")
        courses=request.POST.get("courses","[]")
        scores=json.loads(request.POST.get("scores","[]"))
        retake_classroom=request.POST.get("retake_classroom")
        course_time=request.POST.get("course_time")

        profile,created =student.objects.get_or_create(student_name=student_name)
        profile.courses=courses
        profile.scores=scores
        profile.retake_classroom=retake_classroom
        profile.course_time=course_time
        profile.save()

        return JsonResponse({"message":"Student saved successfully"})
    return JsonResponse({"message":"Invalid request method"},status=400)

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = student.objects.all()
    serializer_class = studentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = student.objects.all()
    serializer_class = studentSerializer
    lookup_field = 'id'

class StudentPostView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            data=request.data
            action=data.get('action') #增加、更新和删除
            if action=='create':
                serializer=studentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            elif action=='update':
                student_id=data.get('id')
                Student=student.objects.get(id=student_id)
                serializer=studentSerializer(Student,data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif action=='delete':
                student_id=data.get('id')
                Student=student.student.objects.get(id=student_id)
                Student.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error':'无效操作'},status=status.HTTP_400_BAD_REQUEST)
        except student.DoesNotExist:
            return Response({'error':'学生不存在'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
