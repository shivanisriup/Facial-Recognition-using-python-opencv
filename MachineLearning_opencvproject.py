from tkinter import *
import sqlite3
import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
det = cv2.CascadeClassifier(r'C:\Users\Harshita\AppData\Local\Programs\Python\Python37\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
class My_gui:
    def __init__(self):
        self.connection = sqlite3.connect("face_recognition.db")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("create table USER(Name varchar(30),Password varchar(20),Address  varchar(20),Contact varchar(10),Email varchar(30))")
            self.connection.commit()
        except:
            pass
            #self.show()
            self.login()
            self.connection.close()



    def train_data(self):
        global model
        global images
        global c
        global d
        global e
        data_path = 'C:/Users/Harshita/Downloads/opencv_proj/faces/'
        only_files=[f for f in listdir(data_path) if isfile(join(data_path,f))]
        e=only_files
        Training_data,Labels=[],[]

        for i,files in enumerate(only_files):
            image_path=data_path+only_files[i] #i has file values
            images=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            Training_data.append(np.asarray(images,dtype=np.uint8))
            c=(Training_data)
            Labels.append(i)
            d=(Labels)

        Labels=np.asarray(Labels,dtype=np.int32)

        #Now build a model

        model=cv2.face.LBPHFaceRecognizer_create() # Linear Binary Face Histogram face_recognizer

        m=model.train(np.asarray(Training_data),np.asarray(Labels))
        b=('Model training completed successfully !!!')
        self.top = Toplevel(self.scr)
        self.top.geometry("300x300")
        msg=Message(self.top,text=b)
        msg.config(bg="yellow", font=('times', 30, 'bold'))
        msg.pack(fill=BOTH,expand=12)
        b3 = Button(self.top, text="Training Data", command=self.training_data, font=('times', 25, 'bold'), bg="white",
                    fg="black")
        b3.place(x=200, y=450)
        b3 = Button(self.top, text="Labels", command=self.labels, font=('times', 25, 'bold'), bg="white",
                    fg="black")
        b3.place(x=800, y=450)
        b3 = Button(self.top, text="Sample Data Set", command=self.sample_data, font=('times', 25, 'bold'), bg="white",
                    fg="black")
        b3.place(x=500, y=450)
        msg.mainloop()
        self.top.mainloop()

    def sample_data(self):
        self.top3 = Toplevel(self.scr)
        self.top3.geometry("300x300")
        msg = Message(self.top3, text=e)
        msg.config(bg="yellow", font=('times', 30, 'bold'))
        msg.pack(fill=BOTH, expand=12)
        self.top3.mainloop()

    def labels(self):
        global top1
        self.top1 = Toplevel(self.scr)
        self.top1.geometry("600x600")
        msg = Message(self.top1, text=d)
        msg.config(bg="green2", font=('times', 28, 'bold'))
        msg.pack(fill=BOTH, expand=12)
        self.top1.mainloop()

    def training_data(self):
        global top2
        self.top2 = Toplevel(self.top)
        self.top2.geometry("800x1000")
        scrollbar = Scrollbar(self.top2)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list = Listbox(self.top2, width=71, height=20, font=('times', 20, 'bold'),
                            yscrollcommand=scrollbar.set)
        for i in c:
            self.list.insert(END, i)
        self.list.bind("student_list", self.show_records)
        self.list.pack(side=TOP, fill=Y)

        scrollbar.config(command=self.list.yview)
        self.top2.mainloop()

    def show_records(self):
        global m
        m = self.list.curselection()
        m = self.list.get(m)
        self.id.delete(0, END)
        self.list.insert(END,c)

    def open_cv(self,img):
        self.gr = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.face = det.detectMultiScale(self.gr, 1.1, 5)
        if self.face is ():
            return None
        for x, y, w, h in self.face:
            cropped_image = self.img#[y:y + h, x:x + w]
        return cropped_image

    def take_image(self):
        cam = cv2.VideoCapture(0)
        count = 0
        while 1:
            self.result, self.img = cam.read()
            if self.open_cv(self.img) is not None:
                count += 1
                face=cv2.resize(self.open_cv(self.img),(200,200))
                face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                file_name_path = 'C:/Users/Harshita/Downloads/opencv_proj/faces/user'+str(count)+'.jpg'
                cv2.imwrite(file_name_path,face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('face cropper',face)
            else:
                print('Face Not Found')
                pass

            if cv2.waitKey(1)== ord('q') or count==100:
                break

        cam.release()
        cv2.destroyAllWindows()

    def face_recogniser(self,img,size=0.5):
        gr = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            #print(gr)
        face = det.detectMultiScale(gr, 1.1, 5)
            #print(faces)
        if face is ():
            return self.img, []

        for (x, y, h, w) in face:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = self.img[y:y + h, x:x + h]
            roi = cv2.resize(roi, (200, 200))
        return self.img, roi

    def show(self):
        global f
        cam = cv2.VideoCapture(0)
        while 1:
            self.ret, self.img = cam.read()
            self.image,self.face = self.face_recogniser(self.img)
            try:
                self.face = cv2.cvtColor(self.face, cv2.COLOR_BGR2GRAY)
                self.res = model.predict(self.face)
                if self.res[1] < 500:
                    confidence = int(100 * (1 - (self.res[1]) / 300))
                    display_string = str(confidence) + '% confidence it is user'
                cv2.putText(self.image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)
                if confidence > 75:
                    f='present'
                    cv2.putText(self.image, f , (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Cropper',self.image)
                else:
                    cv2.putText(self.image, 'Absent', (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Cropper',self.image)
            except:
                cv2.putText(self.image, 'Face not found', (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', self.image)
                pass

            if cv2.waitKey(1)== ord('q') :
                break
        cam.release()
        cv2.destroyAllWindows()

    def login(self):
        global  scr
        self.scr=Tk()
        self.f1 = Frame(self.scr, bg='brown1')
        self.f1.pack(fill=BOTH,expand=25)
        l1 = Label(self.f1, text="WELCOME TO LOGIN PAGE", font=('times', 25, 'bold'), bg="blue", fg="white")
        l1.pack(side=TOP,fill=X)
        l1 = Label(self.f1, text="Name", font=('times', 25, 'bold'), bg="white", fg="black")
        l1.pack()
        self.Id = StringVar()
        e1 = Entry(self.f1, relief="sunken", textvariable=self.Id, font=('times', 25, 'bold'))
        e1.pack()
        l2 = Label(self.f1, text="Password", font=('times', 25, 'bold'), bg="white", fg="black")
        l2.pack()
        self.password = StringVar()
        e2 = Entry(self.f1, relief="sunken", textvariable=self.password, font=('times', 25, 'bold'))
        e2.pack()
        b = Button(self.f1, text="LOGIN", command=self.take_image, font=('times', 25, 'bold'), bg="white",
                   fg="black")
        b.place(x=450,y=250)
        b1 = Button(self.f1, text="REGISTER", command=self.register, font=('times', 25, 'bold'), bg="white",
                   fg="black")
        b1.place(x=650, y=250)
        b2 = Button(self.f1, text="TRAINING_DATA", command=self.train_data, font=('times', 25, 'bold'), bg="white",
                    fg="black")
        b2.place(x=350, y=350)
        b3 = Button(self.f1, text="FACE DETECTOR", command=self.show, font=('times', 25, 'bold'), bg="white",
                    fg="black")
        b3.place(x=700, y=350)

        self.scr.mainloop()

    def register(self):
        global e1
        global e2
        global e3
        global e4
        global e5
        self.scr1 = Tk()
        self.f2 = Frame(self.scr1, bg='yellow')
        self.f2.pack(fill=BOTH, expand=25)
        l = Label(self.f2, text="Register Your Details Here", font=('times', 25, 'bold'), bg="red", fg="white")
        l.pack(side=TOP,fill=X)
        l1 = Label(self.f2, text="Name", font=('times', 25, 'bold'), bg="white", fg="black")
        l1.pack()
        e1 = Entry(self.f2, relief="sunken", font=('times', 25, 'bold'))
        e1.pack()
        l2 = Label(self.f2, text="Password", font=('times', 25, 'bold'), bg="white", fg="black")
        l2.pack()
        e2 = Entry(self.f2, relief="sunken", font=('times', 25, 'bold'))
        e2.pack()
        l3 = Label(self.f2, text="Address", font=('times', 25, 'bold'), bg="white", fg="black")
        l3.pack()
        e3 = Entry(self.f2, relief="sunken", font=('times', 25, 'bold'))
        e3.pack()
        l4 = Label(self.f2, text="Contact", font=('times', 25, 'bold'), bg="white", fg="black")
        l4.pack()
        e4 = Entry(self.f2, relief="sunken", font=('times', 25, 'bold'))
        e4.pack()
        l5 = Label(self.f2, text="E-mail", font=('times', 25, 'bold'), bg="white", fg="black")
        l5.pack()
        e5 = Entry(self.f2, relief="sunken", font=('times', 25, 'bold'))
        e5.pack()
        b = Button(self.f2, text="Submit", command=self.login, font=('times', 25, 'bold'), bg="white",
                   fg="black")
        b.place(x=575,y=500)


My_gui()