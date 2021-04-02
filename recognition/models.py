from django.db import models


# Create your models here.


class Recognition(models.Model):
    sId = models.IntegerField(primary_key=True)
    requestTime = models.DateTimeField(blank=True, null=True)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=20, blank=True, null=True)
    lname = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    cls = models.CharField(max_length=20, blank=True, null=True)
    residence = models.CharField(max_length=50, blank=True, null=True)
    fathername = models.CharField(max_length=20, blank=True, null=True)
    contact = models.IntegerField(default=0)
    time = models.DateTimeField(blank=True, null=True)
    totalAttendance = models.IntegerField(default=0)


class Attendance(models.Model):
    Id = models.IntegerField(primary_key=True)
    inTime = models.DateTimeField(blank=True, null=True)
    outTime = models.DateTimeField(blank=True, null=True)


class CameraMonitor(models.Model):
    timestamp = models.IntegerField(blank=True, null=True)
    browserUniqueName = models.CharField(max_length=100, blank=True, null=True)
    isNeedToStopCamera = models.BooleanField(default=False)
