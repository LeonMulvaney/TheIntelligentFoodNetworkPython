from firebase import firebase
import json
import RPi.GPIO as GPIO
import SimpleMFRC522
import time
GPIO.setwarnings(False)

firebase = firebase.FirebaseApplication('https://{pathToFirebase}',None)

#Resources -----
#Firebase & Python Overview From: https://pypi.python.org/pypi/python-firebase/1.2
#Get Dictionary Values at index from : https://stackoverflow.com/questions/15114843/accessing-dictionary-value-by-index-in-python
#Firebase adding using post From: https://www.youtube.com/watch?v=ZAOTe7MhNSo
#From: https://pimylifeup.com/raspberry-pi-rfid-rc522/
#Split String - From: http://www.pythonforbeginners.com/dictionary/python-split
#Extra Resource: https://github.com/thisbejim/Pyrebase

reader = SimpleMFRC522.SimpleMFRC522()
userId = "{userId}"

while True:
    try:
        result = firebase.get('Users/'+userId+'/foodItems',None) #Get the values from foodItems and save into dict

        #Check if dict is empty From: https://stackoverflow.com/questions/23177439/python-checking-if-a-dictionary-is-empty-doesnt-seem-to-work
        if bool(result) == False:
            print "No Items linked to user account"
            id,text = reader.read()
            foodType,expiryDate,category,empty= text.split(",")
            print ("Tag Id: " + str(id))
            print("Food Type: " + foodType)
            print("Expiry Date: " + expiryDate)
            print("Category:" + category)
            print("\n")

            firebase.post('Users/'+userId+'/foodItems',{'tagId':id,
                                     'foodType':foodType,
                                      'expiryDate':expiryDate,
                                      'category':category})
            print "Item Added to Firebase!"


        #If dict is not empty - Must check to see if tag matches (If so, remove the item or add it to Firebase)
        else:    
            dictionaryLength = len(result) #Get the length of result
            #print result 

            #Dict keys as list From: https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
            rootList = [] #Create list called rootList to hold all the item root nodes
            for key in result.keys(): #Iterate and add each key from result dictionary to rootlist (Saving all the keys)
                rootList.append(key)
                
            
            action = "" #Declare action
            print rootList #Print all the keys
            tagIdList = [] #Create a new list to hold tagId's
            for x in range(0,len(result)):
                firebaseTagId = result.values()[x]["tagId"] #Loop and get all the tag id's, then save to tagIdlist
                tagIdList.append(firebaseTagId)
                
                
            print tagIdList #Print all the tag id's

            #Read values from RFID Chip
            id,text = reader.read()
            foodType,expiryDate,category,empty= text.split(",")
            print ("Tag Id: " + str(id))
            print("Food Type: " + foodType)
            print("Expiry Date: " + expiryDate)
            print("Category:" + category)
            
            print("\n")


            #Loop through the tagIdList, check if the scanned tag matches any in the list, if it does, get the root value and remove, else add the new item to database
            for x in range(0,len(tagIdList)):
                
                listTagId = tagIdList[x]
                if id == listTagId:
                    print "Match"
                    action = "remove"
                    firebaseRoot = rootList[x]
                    
                
                else:
                    print "No Match"

            if action == "remove":
                print "Item Removed"
                
                firebase.delete('Users/'+userId+'/foodItems',firebaseRoot)
                
                
            else:
                firebase.post('Users/'+userId+'/foodItems',{'tagId':id,
                                         'foodType':foodType,
                                          'expiryDate':expiryDate,
                                          'category':category})
                print "Item Added to Firebase!"

        
                
    except KeyboardInterrupt:
        break
        print "Keyboard Interrupt"
        GPIO.cleanup()

    
    
  
