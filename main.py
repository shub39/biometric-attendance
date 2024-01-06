import os
from pyfingerprint.pyfingerprint import PyFingerprint

#################################################################################################################
#################################################################################################################

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print('The Fingerprint sensor cant be initialised!\n')
    print(str(e))
    
#################################################################################################################
#################################################################################################################

def clear_database():
    f.clearDatabase()
    data=open('students.txt','w')
    data.close()
    print('All Data Cleared\n')

def enroll_fingerprint():
    data=open('students.txt','a')
    name=str(input("Enter Student Name: "))
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

            # Wait for finger to be read

            while (f.readImage() == False):
                pass

            f.convertImage(0x01)

            result = f.searchTemplate()
            positionNumber = result[0]

            if (positionNumber >= 0):
                print('Fingerprint Already Exists at #' + str(positionNumber+1) + '\n')
                return None
            else:
                print('*Remove Finger*' + '\n')
                print('*Place Finger Again*' + '\n')
                
                # waiting for second read
                while (f.readImage() == False):
                    pass

                f.convertImage(0X02)

                if (f.compareCharacteristics() == 0):
                    print('Fingers Do Not Match, Try again' + '\n')
                    return None

                f.createTemplate()

                positionNumber = f.storeTemplate()

                f.loadTemplate(positionNumber, 0X01)

                characteristics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                
                print('Fingerprint Registered In Position #' + str(positionNumber+1) + '\n')
                data.write(str(positionNumber) + name + ' '+ '\n') 
                data.flush()
                data.close()
    
    except Exception as e:
        data.close()
        print('Operation failed- Exception message: ' + str(e) + '\n')
        return None
        
def attendance():
    print('Attendance Mode\n')
    t1=1
    try:
        while t1!=0:
            print('1. Take reading')
            t1=int(input('Enter your Choice: '))
            if t1==1:
                print('Place Your finger...')
                while (f.readImage() == False):
                    pass
                f.convertImage()  
                result = f.searchTemplate()
                if result[0]==-1:
                    print('No Match Found' + '\n')
                else:
                    print('Found template at position #' + str(result[0]+1) + '\n')
            else:
                return None
    except Exception as e:
        print('Operation Failed- Exception message: '+str(e) + '\n')       

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    t=1
    while t!=0:
        print('Fingerprint Attendance system with raspberry Pi\n')
        print("1. Enroll a new fingerprint")
        print('2. Attendance')
        print("3. Clear Database")
        print('')
        t=str(input('Select Funtion : '))
        if t=='1':
            enroll_fingerprint()
        elif t=='2':
            attendance()    
        elif t=='3':
            clear_database()  
            
        else:
            t=0     

