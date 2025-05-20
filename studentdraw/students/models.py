
from django.db import models
from django.db import utils
import json

from django.contrib.auth.models import User, PermissionsMixin, UserManager
# Create your models here.
from django.utils import timezone

# Create your models here.
class student(models.Model):
    student_name = models.CharField(max_length=100,verbose_name="学生姓名")
    courses=models.JSONField(verbose_name='课程',default=list)
    scores=models.JSONField(verbose_name='成绩',default=list)
    fail_count=models.IntegerField(verbose_name='挂科次数',default=0)
    retake_count=models.IntegerField(verbose_name='重修次数',default=0)
    latest_retake_score=models.IntegerField(verbose_name='最近一次补考成绩',null=True,blank=True)
    retake_classroom=models.CharField(max_length=100,verbose_name='重修教室',null=True,blank=True)
    course_time=models.CharField(max_length=100,verbose_name='课程时间',null=True,blank=True)
    warning_courses=models.JSONField(verbose_name="预警课程",default=list)
    total_courses=models.IntegerField(verbose_name="总课程数",default=0)
    total_fail_courses=models.IntegerField(verbose_name="总不及格课程数",default=0)


    def save(self,*args,**kwargs):
        self.total_courses=len(self.courses)



        self.fail_count=0
        self.retake_count=0
        self.latest_retake_score=None
        self.warning_courses=[]
        self.total_fail_courses=0

        for course,score_list in zip(self.courses,self.scores):
            latest_score=score_list[-1] if score_list else None
            if latest_score is not None and latest_score<60:
                self.total_fail_courses+=1
                self.warning_courses.append(course)

            self.fail_count+=sum(1 for score in score_list if score<60)
            self.retake_count+=max(0,len(score_list)-2)

        if self.scores:
            self.latest_retake_score=self.scores[-1][-1] if self.scores[-1] else None

        self.warning_courses=self.warning_courses if self.warning_courses else ["暂无学业预警"]

        if self.fail_count==1:
            if self.latest_retake_score is None:
                self.retake_classroom = "未补考"
                self.course_time="未补考"
            elif self.latest_retake_score >=60:
                self.retake_classroom="未重修"
                self.course_time="未重修"
            else:
                self.retake_classroom = "未补考"
                self.course_time = "未补考"
        elif 2<=self.fail_count<4:
            self.retake_classroom="未选课"
            self.course_time="未选课"
        elif self.fail_count==4:
            self.retake_classroom="请选择高阶课程认证"
            self.retake_classroom="请选择高阶课程认证"
        else:
            self.retake_classroom=""
            self.course_time=""



        super().save(*args,**kwargs)

    def __str__(self):
        return self.student_name
    class Meta:
        verbose_name="学生画像"
        verbose_name_plural=verbose_name

# Create your models here.
