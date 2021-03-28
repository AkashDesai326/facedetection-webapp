from django.contrib import admin
from .models import User

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "code", "phone_number", "job", "pwd")