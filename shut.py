#!/bin/python
import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
pin_num=4
GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def Shutdown(channel):
    print("1 signal")
    time.sleep(1)
    print("1 sec")
    if not GPIO.input(pin_num):
        print("2 signal")
        os.system("sudo halt")

GPIO.add_event_detect(pin_num, GPIO.FALLING, callback = Shutdown, bouncetime = 200)

while 1:
    time.sleep(1)
