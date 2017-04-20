#!/usr/bin/python


import RPi.GPIO as GPIO
import time
import websocket
import json
import uuid

def sendMessage(messagecontent):
        try:
                ws = websocket.WebSocket()
                ws.connect("ws://blaky.co.uk:9003")
                connectionId =  uuid.uuid4()
                ws.send(json.dumps({
				"userId": str(uuid.uuid4()),
				"messageId": str(uuid.uuid4()),
				"content": messagecontent,
				"operation": "NOTIFICATION"
			}))
                ws.close()
                print "Successfully sent notification"
        except (RuntimeError, TypeError, NameError) as err:
                print "Error: unable to send notification"
                print err

def callback(channel):  
    if GPIO.input(channel):
        print "LED off"
        sendMessage("HELP ME!, I am so thirsty!")
    else:
        print "LED on"
        sendMessage("WOW! Crazy, thanks for the water!")

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
while True:
    # This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
    time.sleep(0.1)
