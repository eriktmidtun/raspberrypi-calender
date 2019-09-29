import RPi.GPIO as GPIO
import time
import uinput
import os

# set the GPIO board nummer mode.
GPIO.setmode(GPIO.BOARD)

# The pins used on the Pi board based on the board mode over
backPin = 7
forwardPin = 12
refreshPin = 11

# Define what the pins are used for
GPIO.setup(backPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(forwardPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(refreshPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# All virtual key presses used
# must have used modprobe uinput in terminal to use
device = uinput.Device([
        uinput.KEY_P,
        uinput.KEY_N,
        uinput.KEY_F5,
        uinput.KEY_T,
        uinput.KEY_LEFTCTRL,
        uinput.KEY_TAB,
        ])


def reboot():
    # Tells the system to kill chromium and reboot system
    os.system('sudo killall chromium-browser')
    os.system('sudo reboot')


def timer(input_button, pin, t):
    # A timer to check how long a button is pressed, and @t is the max time it should use
    button_timer = 0
    start_t = time.time()
    time.sleep(0.01)

    while input_button == False:
        time.sleep(0.2)
        # Calculates the time spent pushing in the button
        end_t = time.time()
        button_timer = end_t - start_t
        # Gets new value for input to check if still pressed
        input_button = GPIO.input(pin)

        # End the loop if the button is not pressed any longer or the timer is over the given time
        if input_button == True or button_timer > t:
            # print('Button press time', button_timer)
            break
    return button_timer


def click(uinput_keys):
    # just for making the code easier to read
    if len(uinput_keys) > 1:
        device.emit_combo(uinput_keys)
        # sleep to not trigger the keys again
        time.sleep(1.0)
    else:
        device.emit_click(uinput_keys[0])
        time.sleep(0.2)


while True:
    # Updates the states of the buttons. True is default, False is pushed.
    
    input_back = GPIO.input(backPin)
    input_forward = GPIO.input(forwardPin)
    input_refresh = GPIO.input(refreshPin)

    # All buttons pressed at the same time
    if input_back == False and input_refresh == False and input_forward == False:
        reboot()
        
    # Back button is pressed
    if input_back == False:
        # Back button pressed for less than the given time
        if timer(input_back, backPin, 0.8) < 0.7:
            click([uinput.KEY_P])

        # The button was pressed a long time
        else:
            click([uinput.KEY_LEFTCTRL, uinput.KEY_TAB])

    # Forward button is pressed
    if input_forward == False:
        click([uinput.KEY_N])

    # Refresh button is pressed
    if input_refresh == False:
        if timer(input_refresh, refreshPin, 2.1) < 2.0:
            click([uinput.KEY_T])
        else:
            click([uinput.KEY_F5])

    # All buttons pressed at the same time
    if input_back == False and input_refresh == False and input_forward == False:
        reboot()
