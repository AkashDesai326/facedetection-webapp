from django.http.response import StreamingHttpResponse
from recognition.camera import FaceDetect
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import Student, CameraMonitor, Recognition, Attendance
from .object_detection import DetectFace


# Create your views here.
def index(request):
    return render(request, 'recognition/home.html')


def gen(camera, timestamp):
    is_attendance_registered = False
    while True:
        frame = camera.track_image()
        if not is_attendance_registered and camera.Id:
            camera.add_attendance(camera.Id)
            is_attendance_registered = True
        # if not CameraMonitor.objects.get(id=timestamp).is_need_to_stop_camera:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def get_and_save_image(request, id:int,name,lname, email,cls,residence,fathername,contact, camera):
    detect_obj = DetectFace(id, name,lname,email,cls,residence,fathername,contact)

    for i in range(detect_obj.sample_num):
        frame, bytes = camera.get_camera_frame()
        detect_obj.gray_and_save_image(frame, i)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytes + b'\r\n\r\n')

    detect_obj.save_details()
    detect_obj.destroy_image()
    camera.stop_camera()
    return render(request, 'recognition/home.html', {"response": "images taken"})


def capture_image(request):
    face_obj = FaceDetect()
    print(request.POST.get('id'))
    return StreamingHttpResponse(
        get_and_save_image(request,
                           int(request.POST.get("id")),
                           request.POST.get("fname"),
                           request.POST.get("lname"),
                           request.POST.get("email"),
                           # request.POST.get("birthdate"),
                           request.POST.get("cls"),
                           request.POST.get("residence"),
                           request.POST.get("fathername"),
                           int(request.POST.get("contact")),
                           face_obj),
        content_type='multipart/x-mixed-replace; boundary=frame')

    # response = FaceDetect().take_image(int(request.POST.get("id")), request.POST.get("name"))
    # return render(request, 'recognition/home.html', {"response": "images taken"})


def get_capture_image_page(request):
    return render(request, 'recognition/captureimage.html')


def train_image(request):
    response = FaceDetect.train_image(326, "ak326")
    return render(request, 'recognition/home.html', {"response": response})


def track_my_image(request):
    current_timestamp = datetime.utcnow().timestamp()
    CameraMonitor.objects.create(timestamp=current_timestamp)
    return StreamingHttpResponse(gen(FaceDetect(), current_timestamp),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def trackimage(request):
    return render(request, 'recognition/response.html')


def close_camera(request):
    timestamp = request.GET.get('timestamp')
    CameraMonitor.objects.filter(id=timestamp).update(field2='cool')
    # CameraMonitor.objects.(id=timestamp)
    response_data = {
        "success": True
    }
    return JsonResponse(response_data)
