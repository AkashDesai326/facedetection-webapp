from django.http.response import StreamingHttpResponse
from recognition.camera import FaceDetect
from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'recognition/home.html')

def gen(camera):
	while True:
		frame = camera.track_image()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture_image(request):
	# return StreamingHttpResponse(gen(FaceDetect()),
	# 				content_type='multipart/x-mixed-replace; boundary=frame')
	response = FaceDetect().take_image(int(request.POST.get("id")), request.POST.get("name"))
	return render( request ,'recognition/home.html' ,{ "response" : "images taken"})

def train_image(request):
	response = FaceDetect.train_image(326, "ak326")
	return render(request, 'recognition/home.html', {"response": response})

def track_my_image(request):
	return StreamingHttpResponse(gen(FaceDetect()),
								 content_type='multipart/x-mixed-replace; boundary=frame')

def trackimage(request):
	return render(request, 'recognition/response.html')