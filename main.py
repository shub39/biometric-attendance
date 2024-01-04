import os
from pyfingerprint.pyfingerprint import PyFingerprint

def enroll_fingerprint():
    data_folder = 'fingerprint_data'

    # Create the data folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Initialize the Fingerprint sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The fingerprint sensor password is incorrect')
    except Exception as e:
        print('Error initializing the fingerprint sensor: ' + str(e))
        return

    # Get the name of the fingerprint holder
    name = input('Enter the name of the fingerprint holder: ')

    # Enroll fingerprint
    try:
        print('Place your finger on the sensor...')
        while not f.readImage():
            pass

        f.convertImage(0x01)
        result = f.searchTemplate()
        position_number = result[0]

        if position_number == -1:
            print('Template not found. Creating a new template...')
            f.createTemplate()
            position_number = f.storeTemplate()
            template_filename = os.path.join(data_folder, 'template_{}.dat'.format(position_number))
            
            # Download the template characteristics
            position_data = f.downloadCharacteristics(position_number)

            with open(template_filename, 'wb') as template_file:
                template_file.write(position_data)

            # Save the name along with the position number
            name_filename = os.path.join(data_folder, 'name_{}.txt'.format(position_number))
            with open(name_filename, 'w') as name_file:
                name_file.write(name)
            print('Fingerprint enrolled successfully. Position Number: {}'.format(position_number))
        else:
            print('Fingerprint already enrolled at position #{}'.format(position_number))
    except Exception as e:
        print('Error enrolling fingerprint: ' + str(e))

if __name__ == '__main__':
    enroll_fingerprint()
