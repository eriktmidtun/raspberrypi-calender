import RPi.GPIO as GPIO
import time
#import uinput
import os

# set the GPIO board nummer mode.
GPIO.setmode(GPIO.BOARD)

# The pins used on the Pi board based on the board mode over
sensorPin = 37
screenPin = 35

# Define what the pins are used for
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(screenPin, GPIO.OUT)

sleepTime = 3

# local values for toggling screen
screenOn = True
GPIO.output(screenPin,GPIO.HIGH)


# if the motion sensing should be on or off
# hardToggle = False

# sends the signal to the screen to turn on/off
def pulseOnOff():
    GPIO.output(screenPin,GPIO.LOW)
    time.sleep(0.4)
    GPIO.output(screenPin,GPIO.HIGH)

#toggle the screen on or of based on current state.
def toggleScreen():
    global screenOn
    if screenOn  == True:
        pulseOnOff();
        #GPIO.output(35,GPIO.LOW)
        screenOn = False
    else:
        pulseOnOff();
        #GPIO.output(35,GPIO.HIGH)
        screenOn  = True
# turn on the screen if it is of

while True:
    
    #defines how long the screen should be on before it toggles of
    
    while screenOn == False: #motion sensing is off
        
        sensorValue = GPIO.input(sensorPin)
    
        # All buttons pressed at the same time
        if sensorValue == True:
            motionDetected = True
         #   print(motionDetected)
            toggleScreen()
            break
        print("s OFF")
        time.sleep(sleepTime)
    
    

    SCREENONFOR = 180
    while screenOn == True: #motion sensing is on
        
        sensorValue = GPIO.input(sensorPin)
    
        if sensorValue == True:
            motionDetected = True
           # print(motionDetected)
            time.sleep(sleepTime)
            break
        
        print(False)
        SCREENONFOR -= 3
      #  print(SCREENONFOR)
        if SCREENONFOR <= 0:
            toggleScreen() # turn of screen
            
        print("s ON")
        time.sleep(sleepTime)
