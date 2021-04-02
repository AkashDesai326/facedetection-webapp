from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('adminpanel/',views.adminpanel, name="adminpanel"),
    path('adminuser/',views.adminuser, name="adminuser"),
    path('admin/profile',views.adminprofile, name="adminprofile"),
    path('adminuser/add',views.addadmin, name="addadmin"),
    path('admin/new',views.addnewadmin, name="addnewadmin"),
    path('admin/delete',views.deleteadmin, name="deleteadmin"),

    path('students/',views.students, name="students"),
    path('student/add',views.addstudent, name="addstudent"),
    path('student/new',views.newstudent, name="newstudent"),
    path('student/delete', views.deletestudent, name="deletestudent"),

    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('authuser/',views.authadmin, name='authuser'),
    path('loadtake', views.loadtake, name="load"),
]