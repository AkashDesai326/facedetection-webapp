from django.contrib import admin
from .models import Admin

@admin.register(Admin)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "code", "phonenumber", "job", "pwd")

