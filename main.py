import os
import time
import csv
from pyfingerprint.pyfingerprint import PyFingerprint

#################################################################################################################
#################################################################################################################

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(str(e))
    
if not os.path.exists('data/'):
    os.makedirs('data/')

date = time.strftime("%d-%m-%Y", time.localtime())    
    
#################################################################################################################
#################################################################################################################

def show_data(): #Shows The number of fingerprints
    print('No of stored Fingerprints: ' + str(f.getTemplateCount()) + '\n')
    
def clear_database(): #Clears the database 
    f.clearDatabase()
    file1 = open('studentdata.csv','w')
    file1.close()
    print('All Data Cleared\n')

def enroll_fingerprint(): #Enroll a new fingerprint
    try:
        if (f.verifyPassword() == False):
            print('Contact Admin\n')
            raise ValueError('The given fingerprint sensor password wrong\n')
    except Exception as e:
            print('Contact Admin\n')
            print('The fingerprint sensor could not be initialized')
            print('Exception message: ' + str(e) + '\n')
            data.close()
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
                roll = str(input('Enter Roll No: '))
                name = str(input('Enter student Name: '))
                writer.writerow([str(positionNumber+1),roll,name])
    except Exception as e:
        print('Operation failed- Exception message: ' + str(e) + '\n')
        return None
        
def attendance(samay): #Take attendance
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
            attendance(samay)
            return None
        else:
            if not os.path.exists(f'data/{date}.csv'):
                with open(f'data/{date}.csv', 'w') as file2:
                    csvout = csv.writer(file2)
                    csvout.writerow(['Roll','Name','Time In','Time Out'])
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
                            print('Roll no: ',roll)
                            print('Name: ',name)
                            print('Time: ',samay)
        with open(f'data/{date}.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            print(rows)
        for i in rows:
            if i[1] != name:
                rows.append([roll,name,samay,'--'])
            else:
                i[3] = samay    
        with open(f'data/{date}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
                                    
    except Exception as e:
        print('Operation Failed- Exception message: '+str(e) + '\n')       

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    t = 1
    while t != 0:
        print('################################################################################')
        print('Fingerprint Attendance system with raspberry Pi\n')
        print("1. Enroll a new fingerprint")
        print('2. Attendance')
        print("3. Clear Database")
        print('4. Show Data')
        t = str(input('Select Funtion : '))
        print('################################################################################')
        if t == '1':
            enroll_fingerprint()
        elif t == '2':
            time_tuple = time.localtime()
            t1 = time.strftime('%H:%M', time_tuple)
            attendance(t1)    
        elif t == '3':
            clear_database()  
        elif t == '4':
            show_data()
        else:
            t = 0     

