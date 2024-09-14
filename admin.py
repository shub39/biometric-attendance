# Script to enroll data and train face dataset
# Run this in GUI through VNC or HDMI

import cv2
import numpy as np
import os
import shutil
import csv
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import evdev
import sys
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint

# Constants
COUNT_LIMIT = 30
POS = (30, 60)
FONT = cv2.FONT_HERSHEY_COMPLEX
HEIGHT = 1.5
TEXTCOLOR = (0, 0, 255)
BOXCOLOR = (255, 0, 255)
WEIGHT = 3
FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = 'dataset'

# Student Details
name = ""
roll = 0
index = 0

# Edit this accordingly
dept = "CSE(DS)"
sem = 3

# Try to initialise the Fingerprint Sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    try:
        f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        print(str(e))
        sys.exit(1)

def main_menu():
    global name, roll
    while True:
        print("\n---------------------------- ADMIN SCRIPT ---------------------------------")
        print("1. Capture Info")
        print("2. Train Image Dataset")
        print("3. Exit Program")
        print("4. Clear Database\n")
        print("-----------------------------------------------------------------------------\n")

        
        option = int(input("\n[INPUT] Enter Your Choice: "))
        if option == 1:
            name = input("[INPUT] Enter Name: ")
            roll = int(input("[INPUT] Enter Roll no: "))
            capture_fingerprint()
            capture_face()
            write_data()
        elif option == 2:
            train_dataset()
        elif option == 3:
            print("\n[BYE] Exiting the program. Goodbye!")
            break
        elif option ==4:
            clear_database()
        else:
            print("\n[E] Invalid choice. Please enter a valid option.\n")
                  
def capture_fingerprint():
    global roll, name, index
    print('\n[INFO] FINGERPRINTS CURRENTLY STORED: ' + str(f.getTemplateCount()) + '\n')
    
    try:
        print('[ACTION] PLACE FINGER...\n')
        sleep(1)
        
        while not f.readImage():
            pass
        
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        
        if positionNumber >= 0:
            print('\n[INFO] Already exists at #' + str(positionNumber + 1) + 'Try Again (y/n): ')
            choice = input("[INPUT] Enter your Choice: \n")
            if choice == "y":
                capture_fingerprint()
            return None
        
        else:
            print('[ACTION] REMOVE FINGER\n')

            while f.readImage():
                pass
            
            print('[ACTION] PLACE FINGER AGAIN\n')
            sleep(0.5)
            
            while not f.readImage():
                pass
            
            f.convertImage(0x02)
            
            if f.compareCharacteristics() == 0:
                print('[E] FINGERPRINTS DONT MATCH. TRY AGAIN? (y/n)\n')
                choice = input("Enter your Choice: ")
                if choice == "y":
                    capture_fingerprint()
                return None
            
            f.convertImage(0x02)
            f.createTemplate()
            positionNumber = f.storeTemplate()
            print('[INFO] FINGERPRINT REGISTERED AT #' + str(positionNumber + 1) + '\n')
            index = str(positionNumber + 1)

    except Exception as e:
        print('[E] CAPTURE FINGERPRINT FAILED - ' + str(e) + '\n')
        return None

def write_data():
    global roll, name, index
    with open("studentdata.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([index, roll, name, dept, sem])
    
    roll = 0
    index = 0
    name = ""
    
    print("[INFO] DATA WRITTEN\n")

def train_dataset():
    print(f"\n[INFO] TRAINING FACE MODEL\n")
    faces, ids = getImagesAndLabels(path)
    trainRecognizer(faces, ids)
    faces_trained = len(set(ids))
    print(f"\n[INFO] {faces_trained} FACES TRAINED.\n")
    
def getImagesAndLabels(path):
    faceSamples = []
    ids = []

    for file_name in os.listdir(path):
        if file_name.endswith(".jpg"):
            id = int(file_name.split(".")[0])
            img_path = os.path.join(path, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces = face_detector.detectMultiScale(img)

            for (x, y, w, h) in faces:
                faceSamples.append(img[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids

def clear_database():
    f.clearDatabase()
    file1 = open('studentdata.csv','w')
    file1.close()
    try:
        shutil.rmtree("old_dataset")
    except OSError as e:
        print("[INFO] NO OLD DATASET FOLDER")
    try:
        shutil.rmtree("dataset")
    except OSError as e:
        print("[INFO] NO DATASET FOLDER")
    print('[INFO] ALL DATA CLEARED\n')
    sleep(2)

def trainRecognizer(faces, ids):
    recognizer.train(faces, np.array(ids))
    if not os.path.exists("trainer"):
        os.makedirs("trainer")
    recognizer.write('trainer/trainer.yml')

def capture_face():
    global roll
    cam = Picamera2()
    cam.preview_configuration.main.size = (640, 360)
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.controls.FrameRate = 24
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()
    count = 0

    while True:
        frame = cam.capture_array()
        cv2.putText(frame, 'Count:' + str(int(count)), POS, FONT, HEIGHT, TEXTCOLOR, WEIGHT)
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_DETECTOR.detectMultiScale(
            frameGray,      
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), BOXCOLOR, 3)
            count += 1 

            if not os.path.exists("dataset"):
                os.makedirs("dataset")
            if not os.path.exists("old_dataset"):
                os.makedirs("old_dataset")
            file_path = os.path.join("dataset", f"{roll}.{count}.jpg")
            if os.path.exists(file_path):
                old_file_path = file_path.replace("dataset", "old_dataset")
                os.rename(file_path, old_file_path)
            cv2.imwrite(file_path, frameGray[y:y + h, x:x + w])

        cv2.imshow('FaceCapture', frame)
        key = cv2.waitKey(100) & 0xff

        if key == 27: 
            break
        elif key == 113:  
            break
        elif count >= COUNT_LIMIT: 
            break

    print("\n[INFO] Exiting Program and cleaning up stuff")
    cv2.destroyAllWindows()
    cam.close()
    
if __name__ == '__main__':
    main_menu()
