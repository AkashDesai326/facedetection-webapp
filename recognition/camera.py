import pandas as pd
import time
import datetime
import cv2, os
import numpy as np
import csv
from imutils.video import VideoStream
from imutils.video import FPS
from PIL import Image
from django.conf import settings
from .models import Student, Attendance


class FaceDetect(object):

    def __init__(self):
        # initialize the video stream, then allow the camera sensor to warm up
        self.vs = VideoStream(src=0).start()
        # start the FPS throughput estimator
        self.fps = FPS().start()

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
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                name = Student.objects.get(id=Id).name

                # aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + name
                attendance.loc[len(attendance)] = [Id, name, date, timeStamp]

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

    # ts = time.time()
    # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    # timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    # Hour, Minute, Second = timeStamp.split(":")
    # # fileName = os.path.join(os.path.join(settings.MEDIA_ROOT,"Attendance"),"Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv")
    # # attendance.to_csv(fileName, index=False)
    # cam.release()
    # cv2.destroyAllWindows()
    # print(attendance)

    def get_camera_frame(self):
        frame = self.vs.frame
        et, jpeg = cv2.imencode('.jpg', frame)
        return frame, jpeg.tobytes()

    def stop_camera(self):
        self.vs.stop()
