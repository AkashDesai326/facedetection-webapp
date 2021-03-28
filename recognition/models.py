from django.db import models

# Create your models here.


class Recognition(models.Model):
    sId = models.IntegerField(primary_key=True)
    requestTime = models.DateTimeField()

class Attendance(models.Model):
    Id = models.IntegerField(primary_key=True)
    inTime = models.DateTimeField()
    outTime = models.DateTimeField()
