import os
import cv2
import numpy as np
from django.conf import settings
from .models import Student
from PIL import Image


class DetectFace:

    def __init__(self, Id, Name,Lname, Email,Cls,Residence,Fathername,Contact, sample_num: int = 50):
        self.xml_file = "haarcascade_frontalface_default.xml"
        self.xml_path = os.path.join(settings.MEDIA_ROOT, self.xml_file)
        self.Id = Id
        self.Name = Name
        self.Lname = Lname
        self.Email = Email
        # self.Birthdate = Birthdate
        self.Cls = Cls
        self.Residence = Residence
        self.Fathername = Fathername
        self.Contact = Contact


        self.sample_num = sample_num
        self.detector = cv2.CascadeClassifier(self.xml_path)
        self.recognizer = cv2.face_LBPHFaceRecognizer.create()
        self.harcascadePath = os.path.join(settings.MEDIA_ROOT, self.xml_path)

    def save_details(self):
        Student.objects.create(fname=self.Name, id=self.Id , lname=self.Lname , email=self.Email, cls=self.Cls, fathername=self.Fathername, contact=self.Contact, residence=self.Residence)

    def gray_and_save_image(self, frame, num):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # saving the captured face in the dataset folder TrainingImage
            cv2.imwrite(
                os.path.join(os.path.join(settings.MEDIA_ROOT, "TrainingImage"), f"{self.Name}.{self.Id}.{num}.jpg"),
                gray[y:y + h, x:x + w])

    def destroy_image(self):
        cv2.destroyAllWindows()

    # def get_training_object(self):
    #     img = self.vs.read()
    #     harcascadePath =
    #     detector = cv2.CascadeClassifier(harcascadePath)
    #     sampleNum = 0
    #     while (True):
    #         # print(type(ret))
    #         # print(img.shape)
    #         # sys.exit()
    #         img = self.vs.frame
    #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         faces = detector.detectMultiScale(gray, 1.3, 5)
    #         for (x, y, w, h) in faces:
    #             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #             # incrementing sample number
    #             sampleNum = sampleNum + 1
    #             # saving the captured face in the dataset folder TrainingImage
    #             cv2.imwrite(
    #                 os.path.join(os.path.join(settings.MEDIA_ROOT, "TrainingImage"), f"{name}.{Id}.{sampleNum}.jpg"),
    #                 gray[y:y + h, x:x + w])
    #         # display the frame
    #         # cv2.imshow('frame', img)
    #         # wait for 100 miliseconds
    #         if cv2.waitKey(200) & 0xFF == ord('q'):
    #             break  # break if the sample number is morethan 100
    #         elif sampleNum > self.sample_num:
    #             break
    #     # res = "Images Saved for ID : " + str(Id) + " Name : " + name
    #     row = [Id, name]
    #     self.vs.stop()
    #     return "image captured"
