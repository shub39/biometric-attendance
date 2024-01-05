import os
from pyfingerprint.pyfingerprint import PyFingerprint

f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

def clear_database():
    f.clearDatabase()
    data=open('students.txt','w')
    data.close()
    print('')

def enroll_fingerprint():
    data=open('students.txt','a')
    name=str(input("Enter Student Name: "))
    #college_roll=str(input("Enter Student Roll no: "))
    try:
        if (f.verifyPassword() == False):
            print('Contact Admin')
            print('')
            raise ValueError('The given fingerprint sensor password wrong')

    except Exception as e:
            print('Contact Admin')
            print('')
            print('The fingerprint sensor could not be initialized')
            print('Exception message: ' + str(e))
            print('') 
            data.close()
            return None

    print('Currently used templates: ' + str(f.getTemplateCount()))
    print('')

    try:
            print('*Waiting For Finger*')
            print('')

            # Wait for finger to be read

            while (f.readImage() == False):
                pass

            f.convertImage(0x01)

            result = f.searchTemplate()
            positionNumber = result[0]

            if (positionNumber >= 0):
                print('Fingerprint Already Exists at #' + str(positionNumber+1))
                print('')
                return None
            else:
                print('*Remove Finger*')
                print('')
                print('*Place Finger Again*')
                print('')

                # waiting for second read
                while (f.readImage() == False):
                    pass

                f.convertImage(0X02)

                if (f.compareCharacteristics() == 0):
                    print('Fingers Do Not Match, Try again')
                    print('')
                    return None

                f.createTemplate()

                positionNumber = f.storeTemplate()

                f.loadTemplate(positionNumber, 0X01)

                characteristics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                
                print('Fingerprint Registered In Position #' + str(positionNumber+1))
                print('')
                data.write(str(positionNumber) + name + ' '+ '\n') 
                data.flush()
                data.close()
    
    except Exception as e:
        data.close()
        print('Operation failed- Exception message: ' + str(e))
        return None
        
def attendance():
    t1=1
    while t1!=0:
        print('1. Take reading')
        print('0. Quit')
        print('Place Your finger...')
        if t1==1:
            while (f.readImage() == False):
                pass
            f.convertImage(0X01)  
            result = f.searchTemplate()
            if result[0]==-1:
                print('No Match Found')
                print('')
                return None
            else:
                print('Found template at position #' + str(result[0]+1))
                print('')    

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    t=1
    while t!=0:
        print("1. Enroll a new fingerprint")
        print('2. Attendance')
        print("3. Clear Database")
        t=str(input('Select Funtion :'))
        if t=='1':
            enroll_fingerprint()
        elif t=='2':
            attendance()    
        elif t=='3':
            clear_database()  
            
        else:
            t=0     

