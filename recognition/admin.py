from django.contrib import admin
from .models import Attendance, Recognition, CameraMonitor, Student


# Register your models here.
class AttedanceModel(admin.ModelAdmin):
    pass


class RecognitionModel(admin.ModelAdmin):
    pass


class CameraMonitoring(admin.ModelAdmin):
    pass


class StudentDetails(admin.ModelAdmin):
    list_display = ("id", "name", "place", "time", "totalAttendance")


admin.site.register(Attendance, AttedanceModel)
admin.site.register(Recognition, RecognitionModel)
admin.site.register(CameraMonitor, CameraMonitoring)
admin.site.register(Student, StudentDetails)
