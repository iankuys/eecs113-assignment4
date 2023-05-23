#!/usr/bin/python
# Assignment 4 #

import threading
import RPi.GPIO as GPIO
import time

# Pin configurations
BTN_G = 25  # Green pushbutton
BTN_R = 18  # Red pushbutton
BTN_Y = 27  # Yellow pushbutton
BTN_B = 22  # Blue pushbutton
LED_G = 5   # Green LED
LED_R = 6   # Red LED
LED_Y = 12  # Yellow LED
LED_B = 13  # Blue LED

# GPIO setup
GPIO.setwarnings(False) # to disable warnings
GPIO.setmode(GPIO.BCM)

GPIO.setup(BTN_G, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Green Button with initial state low
GPIO.setup(BTN_R, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Red Button with initial state low
GPIO.setup(BTN_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Yellow Button with initial state low
GPIO.setup(BTN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Blue Button with initial state low
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_Y, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

# Blink mode control variables
blink_period = 1.0  # Initial blink period set to 1 (in seconds)
blink_active = False  # Flag to indicate if blink mode is active
thread = None  # Reference to the blink thread

# Turn off all LEDs
def turn_off_leds():
    GPIO.output(LED_G, GPIO.LOW)  
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_Y, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)

# Function to handle blinking LEDs in a separate thread
def blink_thread():
    global blink_active, blink_period
    led_state = GPIO.HIGH
    while blink_active:
        led_state = GPIO.HIGH if led_state == GPIO.LOW else GPIO.LOW
        GPIO.output(LED_G, led_state)
        GPIO.output(LED_R, led_state)
        GPIO.output(LED_Y, led_state)
        GPIO.output(LED_B, led_state)
        time.sleep(blink_period / 2.0)

# Function to handle button presses
def handle(pin):
    global blink_active, thread, blink_period
    # Yellow and Blue buttons pressed simultaneously
    if pin == BTN_Y or pin == BTN_B:
        if GPIO.input(BTN_Y) == GPIO.LOW and GPIO.input(BTN_B) == GPIO.LOW:
            if blink_active:
                # Stop blink mode
                blink_active = False
                thread.join()  # Wait for the blink thread to finish
                turn_off_leds()
            else:
                # Start blink mode
                blink_active = True
                thread = threading.Thread(target=blink_thread)
                thread.daemon = True
                thread.start()
    elif pin == BTN_R:
        # Red button pressed, double the blink period
        blink_period *= 2
    elif pin == BTN_G:
        # Green button pressed, halve the blink period
        blink_period /= 2

### Event listener (Tell GPIO Library to look out for an event on each pushbuttton and pass handle function)
# Event listener setup for button presses
GPIO.add_event_detect(BTN_G, GPIO.FALLING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_R, GPIO.FALLING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_Y, GPIO.FALLING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_B, GPIO.FALLING, callback=handle, bouncetime=200)

# Endless loop with delay to wait for events
while True:
    time.sleep(1e6)