from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password

import tkinter as tk
from tkinter import Message ,Text
import cv2
import sys
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def register(request):
    fullname = request.POST.get('fullname')
    print(fullname)
    email = request.POST.get('email')
    code = int(request.POST.get('code'))
    phonenumber = int(request.POST.get('phonenumber'))
    job = request.POST.get('job')
    pwd = request.POST.get('password')
    rpwd = request.POST.get('repeatpwd')

    usr = User.objects.filter(email=email)
    print(usr)
    if len(usr) == 0:
        if(pwd == rpwd):
            pwd = make_password(pwd)
            newuser = User.objects.create(fullname=fullname, email=email, code=code, phone_number=phonenumber,
                                              job=job , pwd=pwd)
            newuser.save()
            return render(request , "login.html")
        else:
            return render(request ,'signup.html', {'error': "password does not match"})
        # products = Product.objects.all()
        # categories = Category.objects.all()
    else:
        return render(request, 'signup.html', {'error': 'This username already exists'})

def login(request):
    return render(request, 'login.html')

def authuser(request):
    user = User.objects.filter(email=request.POST.get('email')).first()
    if user is not None:
        if check_password(request.POST.get('password'), user.pwd):
            request.session['email'] = user.email
            return render( request , 'index.html')
        else:
            return render(request, 'login.html', {'error': 'invalid password'})
    else:
        return render(request, 'login.html', {'error': 'invalid email id'})

def loadtake(request):
    return render(request, 'takeimage.html')

def take(request):
    return HttpResponse('bodfhbdosfvdpsh ')