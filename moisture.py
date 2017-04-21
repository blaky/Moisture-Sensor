#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import websocket
import json
import uuid
import datetime as dt

latestState = None
notificationSentAt = dt.datetime.fromtimestamp(0)

def sendMessage(state):
        global latestState, notificationSentAt
        
        messageContent = "WOW! Crazy, thanks for the water!" if state else "HELP ME!, I am so thirsty!"
        try:
                print "Sending: " + messageContent
                ws = websocket.WebSocket()
                ws.connect("ws://blaky.co.uk:9003")
                connectionId =  uuid.uuid4()
                ws.send(json.dumps({
				"userId": str(uuid.uuid4()),
				"messageId": str(uuid.uuid4()),
				"content": messageContent,
				"operation": "NOTIFICATION"
			}))
                ws.close()

                # Setting globals to prevent message flow.
                notificationSentAt = dt.datetime.now()
                latestState = state
                print "Successfully sent notification for " + ("ON" if state else "OFF") + " state."
        except (RuntimeError, TypeError, NameError) as err:
                print "Error: unable to send notification"
                print err

def callback(channel):
        global latestState, notificationSentAt
        
        state = GPIO.input(channel)
        timeDifference = (dt.datetime.now() - notificationSentAt).seconds
        #print "time difference: " + str(timeDifference)
        #print "current state: " + str(state)
        #print "old state: " + str(latestState)
        if latestState != state and timeDifference > 15:
                sendMessage(state)
        else:
                print "State hasn't changed or too quickly"


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
