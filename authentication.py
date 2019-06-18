import time
from pyfingerprint.pyfingerprint import PyFingerprint

# Sensor initialisation

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if (f.verifyPassword() == False):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

# trying to authenticate

try:
    # Deleting the database
    f.clearDatabase()
	
    # Uploading the template to the sensor
    temp_file = open("template.txt", "r")
    template = []
    template.append(int(temp_file.read()))
    temp_file.close()
    f.uploadCharacteristics(characteristicsData=template)
    positionNumber = f.storeTemplate()
    print('Finger uploaded successfully!')
    print('New template position #' + str(positionNumber))

    # Tries to search the finger
    print('Waiting for finger...')

    # Wait that finger is read
    while ( f.readImage() == False ):
        pass

    # Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    # Searches template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)