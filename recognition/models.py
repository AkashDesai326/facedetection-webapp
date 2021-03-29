from django.db import models


# Create your models here.


class Recognition(models.Model):
    sId = models.IntegerField(primary_key=True)
    requestTime = models.DateTimeField(blank=True, null=True)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    place = models.CharField(max_length=50,blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    total_attendance = models.IntegerField(default=0)


class Attendance(models.Model):
    Id = models.IntegerField(primary_key=True)
    inTime = models.DateTimeField(blank=True, null=True)
    outTime = models.DateTimeField(blank=True, null=True)


class CameraMonitor(models.Model):
    timestamp = models.IntegerField(blank=True, null=True)
    browser_unique_name = models.CharField(max_length=100, blank=True, null=True)
    is_need_to_stop_camera = models.BooleanField(default=False)
