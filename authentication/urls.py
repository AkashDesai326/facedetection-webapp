from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('authuser/',views.authuser, name='authuser'),
    path('loadtake', views.loadtake, name="load"),
]