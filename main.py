# Importing Modules

import os
import time
import csv
import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint

# Keyboard stuff

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialising the fingerprint sensor

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    
except Exception as e:
    f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
    
except Exception as e:
    print(str(e))
    
# Making the data folder
    
if not os.path.exists('data/'):
    os.makedirs('data/')

# Grabbing the time
 
date = time.strftime("%d-%m-%Y", time.localtime())    
    
# Funtions

def readLine(line, characters): # detects keypad input
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        return characters[0]
    if(GPIO.input(C2) == 1):
        return characters[1]
    if(GPIO.input(C3) == 1):
        return characters[2]
    if(GPIO.input(C4) == 1):
        return characters[3]
    GPIO.output(line, GPIO.LOW)

def show_data(): #Shows The number of fingerprints
    print('No of stored Fingerprints: ' + str(f.getTemplateCount()) + '\n')
    
def clear_database(): #Clears the database 
    f.clearDatabase()
    file1 = open('studentdata.csv','w')
    file1.close()
    print('All Data Cleared\n')

def enroll_fingerprint(): #Enrolls a new fingerprint
    try:
        
        if (f.verifyPassword() == False):
            print('Contact Admin\n')
            raise ValueError('The given fingerprint sensor password wrong\n')
            
    except Exception as e:
        
            print('Contact Admin\n')
            print('The fingerprint sensor could not be initialized')
            print('Exception message: ' + str(e) + '\n')
            return None
            
    print('Currently used templates: ' + str(f.getTemplateCount()) + '\n')
    
    try:
        
        print('*Waiting For Finger*' + '\n')
        time.sleep(1)
        
        while (f.readImage() == False):
            pass
            
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        
        if (positionNumber >= 0):
            print('Fingerprint Already Exists at #' + str(positionNumber+1) + '\n')
            time.sleep(2)
            return None
            
        else:
            print('**Remove your finger**\n')
            
            while (f.readImage() == True):
                pass
                
            print('**Place your finger again**\n')    
            time.sleep(1) 
            
            while (f.readImage() == False):
                pass
                
            f.convertImage(0X02)  
              
            if f.compareCharacteristics() == 0:
                print('Fingerprints dont match...Trying again\n')
                time.sleep(2)
                enroll_fingerprint()
                return None
                
            f.convertImage(0X02)
            f.createTemplate()
            positionNumber = f.storeTemplate()
            
            print('Fingerprint Registered In Position #' + str(positionNumber+1) + '\n')
            
            with open('studentdata.csv', 'a') as file1:
                writer = csv.writer(file1)
                roll = str(input('Enter roll No: '))
                name = str(input('Enter student Name: '))
                dept = str(input('Enter department: '))
                year = str(input('Enter Year: '))
                writer.writerow([str(positionNumber+1),roll,name,dept,year])
                
    except Exception as e:
        print('Operation failed- Exception message: ' + str(e) + '\n')
        return None
        
def attendance(samay): #Takes attendance
    print('Registering finger at: ',samay)
    
    try:
        print('Place Your finger...\n')
        time.sleep(1)
    
        while (f.readImage() == False):
            pass
        
        f.convertImage()  
        result = f.searchTemplate()
        
        if result[0] == -1:
            print('No Match Found Try Again...' + '\n')
            return None
        
        else:
            if not os.path.exists(f'data/{date}.csv'):
                with open(f'data/{date}.csv', 'w') as file2:
                    csvout = csv.writer(file2)
                    csvout.writerow(['Roll','Name','Department','Year','Time In','Time Out'])
        
            print('Found template at position #' + str(result[0]+1) + '\n')
        
            with open('studentdata.csv','r') as file1:
                with open(f'data/{date}.csv', 'r') as file2:
                    csvread = csv.reader(file1)
                    csvread2 = csv.reader(file2)
                    csvwrite2 = csv.writer(file2)
        
                    for row in csvread:
                        if row[0] == str(result[0]+1):
                            roll = str(row[1])
                            name = str(row[2])
                            dept = str(row[3])
                            year = str(row[4])
                            print('Roll no: ',roll)
                            print('Name: ',name)
                            print('Department: ',dept)
                            print('Year: ',year)
                            print('Time: ',samay)
        
        with open(f'data/{date}.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        present = 1    
        
        for i in rows:
            if i[1] == name:
                i.append(samay)
                present = 0
                break
        
        if present == 1:
            rows.append([roll,name,dept,year,samay])        
        
        with open(f'data/{date}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
                                    
    except Exception as e:
        print('Operation Failed- Exception message: '+str(e) + '\n')       

# Main Funtion

if __name__ == '__main__':
    
    while True:
        print('################################################################################')
        print('Fingerprint Attendance system with raspberry Pi\n')
        print("1. Enroll a new fingerprint")
        print('2. Attendance in')
        print("3. Attendance out")
        print('################################################################################')
        try:
            while True:
                if readLine(L1, ["1","2","3","A"]) == "1":
                    enroll_fingerprint()
                    break
                    
                elif readLine(L1, ["1","2","3","A"]) == "2" or readLine(L1, ["1","2","3","A"]) == "3":
                    time_tuple = time.localtime()
                    attendance(time.strftime('%H:%M', time_tuple)) 
                    break;
                    
                
                    
               
        except KeyboardInterrupt:
            print("\nApplication stopped!") 

