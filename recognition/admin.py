from django.contrib import admin
from .models import Attendance, Recognition

# Register your models here.
class AttedanceModel(admin.ModelAdmin):
    pass

class RecognitionModel(admin.ModelAdmin):
    pass

admin.site.register(Attendance, AttedanceModel)
admin.site.register(Recognition, RecognitionModel)