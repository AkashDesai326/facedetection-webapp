import pandas as pd
import time
from datetime import datetime
import cv2, os
import numpy as np
import csv
from imutils.video import VideoStream
from imutils.video import FPS
from PIL import Image
from django.conf import settings
from .models import Student, Attendance
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from email.mime.text import MIMEText

if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, "TrainingImage")):
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "TrainingImage"))

if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, "TrainingImageLabel")):
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "TrainingImageLabel"))

if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, "ImagesUnknown")):
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "ImagesUnknown"))

class FaceDetect(object):

    def __init__(self):
        # initialize the video stream, then allow the camera sensor to warm up
        self.vs = VideoStream(src=0).start()
        # start the FPS throughput estimator
        self.fps = FPS().start()
        self.Id = None

    def __del__(self):
        cv2.destroyAllWindows()

    def take_image(self, Id, name):
        img = self.vs.read()
        harcascadePath = os.path.join(settings.MEDIA_ROOT, "haarcascade_frontalface_default.xml")
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            # print(type(ret))
            # print(img.shape)
            # sys.exit()
            img = self.vs.frame
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite(
                    os.path.join(os.path.join(settings.MEDIA_ROOT, "TrainingImage"), f"{name}.{Id}.{sampleNum}.jpg"),
                    gray[y:y + h, x:x + w])
            # display the frame
            # cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(200) & 0xFF == ord('q'):
                break  # break if the sample number is morethan 100
            elif sampleNum > 50:
                break
        cv2.destroyAllWindows()
        # res = "Images Saved for ID : " + str(Id) + " Name : " + name
        row = [Id, name]
        with open(os.path.join(settings.MEDIA_ROOT, 'StudentDetails.csv'), 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        self.vs.stop()
        return "image captured"

    @classmethod
    def getImagesAndLabels(cls, path):
        # get the path of all the files in the folder
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # print(imagePaths)

        # create empth face list
        faces = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids

    @classmethod
    def train_image(cls, Id, name):
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = os.path.join(settings.MEDIA_ROOT, "haarcascade_frontalface_default.xml")
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, id = cls.getImagesAndLabels(os.path.join(settings.MEDIA_ROOT, "TrainingImage"))
        print(id)
        recognizer.train(faces, np.array(id))
        recognizer.save(os.path.join(os.path.join(settings.MEDIA_ROOT, "TrainingImageLabel"), "Trainner.yml"))
        return "Image Trained"  # +",".join(str(f) for f in Id)

    def track_image(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        recognizer.read(os.path.join(os.path.join(settings.MEDIA_ROOT, "TrainingImageLabel"), "Trainner.yml"))
        harcascadePath = os.path.join(settings.MEDIA_ROOT, "haarcascade_frontalface_default.xml")
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        # df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, "StudentDetails.csv"))
        self.vs.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)
        im = self.vs.frame
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                name = Student.objects.get(id=Id).fname
                tt = str(Id) + "-" + name
                attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                if Id:
                    self.Id = Id
            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                noOfFile = len(os.listdir((os.path.join(settings.MEDIA_ROOT, "ImagesUnknown")))) + 1
                cv2.imwrite(os.path.join(os.path.join(settings.MEDIA_ROOT, "ImagesUnknown"), f"{Image}{noOfFile}.jpg"),
                            im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        et, jpeg = cv2.imencode('.jpg', im)
        return jpeg.tobytes()

    def get_camera_frame(self):
        frame = self.vs.frame
        et, jpeg = cv2.imencode('.jpg', frame)
        return frame, jpeg.tobytes()

    def stop_camera(self):
        self.vs.stop()

    def add_attendance(self, Id):
        start_date = datetime.utcnow()
        today_date = datetime(start_date.year, start_date.month, start_date.day)

        db_object = Attendance.objects.filter(inTime__gte=today_date, Id=Id)
        if db_object:
            try:
                field_value = getattr(db_object[0], "outTime")
            except AttributeError:
                field_value = None
            if field_value is None:
                student_obj = Student.objects.get(id=int(Id))
                if student_obj:
                    total_attendance = student_obj.totalAttendance
                    total_attendance += 1
                    # sender_email = "akashdesai428@gmail.com"
                    # password = 'gmail@428'
                    # msg = MIMEMultipart('alternative')
                    # receiver_email = 'akashdesai428@gmail.com'
                    # msg['Subject'] = "Visualize"
                    # msg['From'] = sender_email
                    # msg['To'] = 'akashdesai428@gmail.com'
                    #
                    # # Create the body of the message (a plain-text and an HTML version).
                    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
                    # time_stamp = time.time()
                    # params = {'stamp': f'{time_stamp}'}
                    # html = """\
                    #         <html>
                    #           <head></head>
                    #           <body>
                    #             <p>Hi!<br>
                    #                Reset your password from below link<br>
                    #                <hr>
                    #                <a href="http://127.0.0.1:8000/dashboard/reset/password/form/""" + """">Reset your Password</a> you wanted.
                    #             </p>
                    #           </body>
                    #         </html>
                    #         """
                    # part1 = MIMEText(text, 'plain')
                    # part2 = MIMEText(html, 'html')
                    # msg.attach(part1)
                    # msg.attach(part2)
                    # context = ssl.create_default_context()
                    # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    #     server.login(sender_email, password)
                    #     server.sendmail(
                    #         sender_email, receiver_email, msg.as_string()
                    #     )

                    Student.objects.filter(id=int(Id)).update(totalAttendance=total_attendance)
                Attendance.objects.filter(inTime__gte=today_date, Id=Id).update(outTime=start_date)
            else:
                pass
        else:
            Attendance.objects.create(Id=Id, inTime=start_date)