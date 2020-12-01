from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Student(models.Model):
    FSUID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    major = models.CharField(max_length=50)
    semester = models.IntegerField()

    def __str__(self):
        return self.FSUID.username

class Professor(models.Model):
    FSUID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    office = models.CharField(max_length=10, blank=True) 

    def __str__(self):
        return self.FSUID.username

class Class(models.Model):
    course_reference_number = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=60)        #i.e., Programming I
    description = models.TextField(blank=True)   
    subject_id = models.CharField(max_length=3)   #i.e., COP
    number_id = models.CharField(max_length=4)    #i.e., 3014 (combined w/ line above makes COP3014)
    section = models.IntegerField()
    semester = models.CharField(max_length=6, default="Spring")     # values: FALL, SPRING, SUMMER
    year = models.IntegerField(default=2021)                  # i.e., 2021
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    CSBS_Req = models.BooleanField(default=False)
    CSBS_Elec = models.BooleanField(default=False)
    CSBA_Req = models.BooleanField(default=False)
    CSBA_Elec = models.BooleanField(default=False)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    date_start = models.DateField(default=date(2021, 1, 6))
    date_end = models.DateField(default=date(2021, 4, 23))
    enrollment_capacity = models.IntegerField()
    enrollment_number = models.IntegerField(default=0)
    location = models.CharField(max_length=10, blank=True) 
    hasRecitation = models.BooleanField(default=False)
    recitation_time_start = models.TimeField(null=True, blank=True)
    recitation_time_end = models.TimeField(null=True, blank=True)
    recitation_location = models.CharField(max_length=10, blank=True)  
    recommended_semester = models.IntegerField(null=True, blank=True)
    lec_mo = models.BooleanField(default=False)
    lec_tu = models.BooleanField(default=False)
    lec_we = models.BooleanField(default=False)
    lec_th = models.BooleanField(default=False)
    lec_fr = models.BooleanField(default=False)
    rec_mo = models.BooleanField(default=False)
    rec_tu = models.BooleanField(default=False)
    rec_we = models.BooleanField(default=False)
    rec_th = models.BooleanField(default=False)
    rec_fr = models.BooleanField(default=False)
    lec_days = models.CharField(max_length=14, blank=True)
    rec_day = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.subject_id + self.number_id + '-' + str(self.section).zfill(4) + ' (#' + self.course_reference_number + ')'


class Enrolled_In(models.Model):
    FSUID = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_reference_number = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.FSUID) + ' - ' + self.course_reference_number.course_reference_number
        



