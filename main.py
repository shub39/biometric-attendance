# Main script, handles attendance
# no GUI required, can be autorun or run via ssh

import os
import time
import csv
from keypad import read_keypad
# import display
import evdev
import sys
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
import threading
import queue
import cv2
import numpy as np
from picamera2 import Picamera2

# Subject
subject = ""

# Constants for Camera
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8)
recognizer.read('trainer/trainer.yml')
box_color = (255, 0, 255)
cam = Picamera2()
cam.start()

# Queue for multithreading
result_queue = queue.Queue()

# Names list for 61 students (Edit according to your class size)
names = [str(i) for i in range(1, 61)]

# Initialising the fingerprint sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(f"[E] CANT INITIALISE SENSOR: {str(e)}")

# Making the data folder
if not os.path.exists('data/'):
    os.makedirs('data/')

# Grabbing the time
date = time.strftime("%d-%m-%Y", time.localtime())

# FUNCTIONS
# Select Subject
def subject_select():
    global subject
    # display.draw([
    # "SELECT SUBJECT",
    # "1 - CHEMISTRY",
    # "2 - MATHEMATICS",
    # "3 - COMP",
    # "4 - ENGLISH"
    # ])
    print("\n[S] SELECT SUBJECT")
    print("[S] 1 - CHEMISTRY")
    print("[S] 2 - MATHEMATICS")
    print("[S] 3 - COMP")
    print("[S] 4 - ENGLISH")

    sleep(1)

    while True:
        if read_keypad() == "1":
            subject = "CHEMISTRY"
            break
        if read_keypad() == "2":
            subject = "MATHEMATICS"
            break
        if read_keypad() == "3":
            subject = "COMP"
            break
        if read_keypad() == "4":
            subject = "ENGLISH"
            break
        sleep(0.1)

    # display.draw(["SELECTED", subject])
    print("[S] SELECTED \n" + subject)
    sleep(1)


# Shows The number of fingerprints
def show_data():
    print('\n[SD] COUNT: ' + str(f.getTemplateCount()) + '\n')
    print(f"[SD] SUBJECT: {subject}\n")
    # display.draw([
    # "COUNT: " + str(f.getTemplateCount()),
    # "SUBJECT: " + subject
    # ])
    sleep(2)


# Clears the database 
def clear_database():
    f.clearDatabase()
    # display.draw(["DATA CLEARED"])
    file1 = open('studentdata.csv', 'w')
    file1.close()
    print('[D] All Data Cleared\n')
    sleep(3)


def fingerprint_attendance():
    time_tuple = time.localtime()
    samay = time.strftime('%H:%M', time_tuple)

    try:
        print('\n[FA] PLACE FINGER...')
        time.sleep(1)
        print("[FA] SUBJECT: ", subject)
        print("[FA] TIME: ", samay)
        print("[FA] DATE: ", date)

        while (f.readImage() == False):
            pass

        f.convertImage()
        result = f.searchTemplate()

        if result[0] == -1:
            print('[FA] NO MATCH TRY AGAIN' + '\n')
            fingerprint_attendance()
            return None

        else:
            print('[FA] FOUND FINGERPRINT ' + str(result[0] + 1) + '\n')
            result_queue.put(('fingerprint', result[0] + 1))
            return result[0] + 1

    except Exception as e:
        print("[E] ERROR DETECTING FINGERPRINT", e)

def face_attendance():
    while True:
        frame = cam.capture_array()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_detector.detectMultiScale(
            frame_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            name_pos = (x + 5, y - 5)
            conf_pos = (x + 5, y + h + 20)
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 3)
            
            id, confidence = recognizer.predict(frame_gray[y:y + h, x:x + w])

            if id >= len(names) or id < 0:
                detected_name = "unknown"
                confidence = "N/A"
            else:
                detected_name = names[id]
                confidence = f"{100 - confidence:.0f}%"

            print(f"[FAA] Detected ID: {detected_name}, Confidence: {confidence}")

            if isinstance(confidence, str) or int(confidence[:-1]) > 50:
                print("\n[FAA] Exiting Program and cleaning up stuff")
                result_queue.put(('face', id))
                return id

def write_data(roll = 0, index = 0):
    name = ''
    dept = ''
    sem = ''
    
    time_tuple = time.localtime()
    samay = time.strftime('%H:%M', time_tuple)
    print('\n[WD] TIME: ', samay)
    
    if not os.path.exists(f'data/{date}_{subject}.csv'):
        with open(f'data/{date}_{subject}.csv', 'w') as file2:
            csvout = csv.writer(file2)
            csvout.writerow(['Roll', 'Name', 'Subject', 'Time In', 'Time Out'])

    if index != 0:
        print('[WD] FOUND FINGERPRINT AT ' + str(index) + '\n')
        with open('studentdata.csv', 'r') as file1:
            with open(f'data/{date}_{subject}.csv', 'r') as file2:
                csvread = csv.reader(file1)
                csvread2 = csv.reader(file2)
                csvwrite2 = csv.writer(file2)

                for row in csvread:
                    if row[0] == str(index):
                        roll = str(row[1])
                        name = str(row[2])
                        dept = str(row[3])
                        sem = str(row[4])
                        print('\n[WD] Roll no: ', roll)
                        print('[WD] Name: ', name)
                        print('[WD] Department: ', dept)
                        print('[WD] Sem: ', sem)
                        print('[WD] Time: ', samay)

        # display.draw([
        # "REGISTERING...",
        # "NAME: " + name,
        # "ROLL: " + roll,
        # "DEPT: " + dept,
        # "SEM: " + year    
        # ])        

    else:
        print(f"[WD] FOUND FACE AT {roll}\n")
        with open('studentdata.csv', 'r') as file1:
            with open(f'data/{date}_{subject}.csv', 'r') as file2:
                csvread = csv.reader(file1)
                csvread2 = csv.reader(file2)
                csvwrite2 = csv.writer(file2)

                for row in csvread:
                    if row[1] == str(roll):
                        roll = str(row[1])
                        name = str(row[2])
                        dept = str(row[3])
                        sem = str(row[4])
                        print('\n[WD] Roll no: ', roll)
                        print('[WD] Name: ', name)
                        print('[WD] Department: ', dept)
                        print('[WD] Sem: ', sem)
                        print('[WD] Time: ', samay)

    with open(f'data/{date}_{subject}.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    present = 1

    for i in rows:
        if i[1] == name:
            i.append(samay)
            present = 0
            break

    if present == 1:
        rows.append([roll, name, subject, samay])

    with open(f'data/{date}_{subject}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def attendance():

    if subject == "":
        subject_select()

    def fingerprint_thread():
        fingerprint_attendance()

    def face_thread():
        face_attendance()

    thread1 = threading.Thread(target=face_thread)
    thread2 = threading.Thread(target=fingerprint_thread)

    thread1.start()
    thread2.start()

    result_type, result_value = result_queue.get()

    print(f"[A] First to finish: {result_type} with value: {result_value}")

    if result_type == 'fingerprint':
        write_data(index=result_value)
    else:
        write_data(roll=result_value)

# Main Menu
def main_menu():
    print("\n1 - ATTENDANCE")
    print("2 - SELECT SUBJECT")
    print("3 - SHOW DATA")
    print("4 - SHUT DOWN\n")

    while True:
        # display.draw([
        # "1 - ATTENDANCE",
        # "2 - SELECT SUBJECT",
        # "3 - SHOW DATA",
        # "4 - SHUT DOWN"
        # ])

        if read_keypad() == "1":
            attendance()
        elif read_keypad() == "2":
            subject_select()
        elif read_keypad() == "3":
            show_data()
        elif read_keypad() == "4":
            return 1


# Main Function
if __name__ == '__main__':
    if main_menu() == 1:
        os.system("sudo shutdown now")
        sys.exit()
