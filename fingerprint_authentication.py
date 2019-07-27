#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
from pyfingerprint.pyfingerprint import PyFingerprint
import sesame_client

api_key =os.environ['SESAME_KEY'] 

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
while True:
    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
        else:
            sesames = sesame_client.SesameClient(api_key)
            #sesames.get_status()
            result = sesames.unlock_all()
            print("unlock:" + result)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)