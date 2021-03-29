from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('adminpanel/',views.adminpanel, name="adminpanel"),
    path('adminuser/',views.adminuser, name="adminuser"),
    path('adminuser/add',views.addadmin, name="addadmin"),
    path('admin/new',views.addnewadmin, name="addnewadmin"),
    path('admin/delete',views.deleteadmin, name="deleteadmin"),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('authuser/',views.authadmin, name='authuser'),
    path('loadtake', views.loadtake, name="load"),
]