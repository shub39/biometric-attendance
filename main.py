import os
import csv
from pyfingerprint.pyfingerprint import PyFingerprint

#################################################################################################################
#################################################################################################################

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print('The Fingerprint sensor can not be initialised!\n')
    print(str(e))
    
#################################################################################################################
#################################################################################################################

def show_data():
    print('No of stored Fingerprints: ' + str(f.getTemplateCount()) + '\n')
    
def clear_database():
    f.clearDatabase()
    file1 = open('studentdata.csv','w')
    file1.close()
    print('All Data Cleared\n')

def enroll_fingerprint():
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
        while (f.readImage() == False):
            pass
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        if (positionNumber >= 0):
            print('Fingerprint Already Exists at #' + str(positionNumber+1) + '\n')
            return None
        else:
            print('**Remove your finger**\n')
            while (f.readImage() == True):
                pass
            print('**Place your finger again**\n')    
            while (f.readImage() == False):
                pass
            f.convertImage(0X02)    
            if f.compareCharacteristics() == 0:
                print('Fingerprints dont match...Trying again\n')
                enroll_fingerprint()
                return None
            f.convertImage(0X02)
            f.createTemplate()
            positionNumber = f.storeTemplate()
            print('Fingerprint Registered In Position #' + str(positionNumber+1) + '\n')
            file1=open('studentdata.csv','a')
            writer=csv.writer(file1)
            roll=str(input('Enter Roll No: '))
            name=str(input('Enter student Name: '))
            writer.writerow([str(positionNumber+1),roll,name])
            file1.close()
    except Exception as e:
        print('Operation failed- Exception message: ' + str(e) + '\n')
        return None
        
def attendance():
    try:
        print('Place Your finger...\n')
        while (f.readImage() == False):
            pass
        f.convertImage()  
        result = f.searchTemplate()
        if result[0]==-1:
            print('No Match Found Try Again...' + '\n')
            attendance()
        else:
            print('Found template at position #' + str(result[0]+1) + '\n')
            file1 = open('studentdata.csv','r')
            csvreader = csv.reader(file1)
            for row in csvreader:
                if row[0] == str(result[0]+1):
                    print(row)
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
            attendance()    
        elif t == '3':
            clear_database()  
        elif t == '4':
            show_data()
        else:
            t = 0     

