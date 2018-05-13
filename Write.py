import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

while True:
        try:
                foodType = raw_input('Food Type: ')
                expiryDate = raw_input('Expiry Date: ')
                category = raw_input('Category:')
                data = str(foodType+","+expiryDate+","+category+",")
                print ("Now place your tag to write")
                reader.write(data)
                print("Written")
                id,text = reader.read()
                print(text)
                print "---------------------------"
                print "---------New Item---------"
                print "---------------------------"

        finally:
                GPIO.cleanup()
