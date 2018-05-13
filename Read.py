#From: https://pimylifeup.com/raspberry-pi-rfid-rc522/
#Split String - From: http://www.pythonforbeginners.com/dictionary/python-split

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
from firebase import firebase

reader = SimpleMFRC522.SimpleMFRC522()



while True:
    try:
        id,text = reader.read()
        print("TAG ID: " + str(id))
        foodType,expiryDate,category,empty= text.split(",")
        print("Food Type: " + foodType)
        print("Expiry Date: " + expiryDate)
        print("Category: " + category)
        print("\n")
        time.sleep(3)


    except KeyboardInterrupt:
        GPIO.cleanup()

    
    
  
