from django.urls import path, include
from recognition import views

urlpatterns = [
    path('', views.index, name='index'),
    path('capture_image', views.capture_image, name='capture_image'),
    path('train_image', views.train_image, name='train_image'),
    path('track_image', views.track_my_image, name='track_image'),
    path('trackimage', views.trackimage, name='trackimage'),
    path('closecamera', views.close_camera, name="closecamera"),
]
