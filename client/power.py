#!/usr/bin/python
#-*- coding: utf-8; -*-

import RPi.GPIO as GPIO
import time
SW=26
LED=16
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
status=0

def power(sw_gpio,led_gpio,status):
    sw=GPIO.input(sw_gpio)
    if sw==1 and status==1:
        GPIO.output(led_gpio,GPIO.HIGH)
        status=0
        sw=0
        time.sleep(0.5)
    if sw==1 and status==0:
        GPIO.output(lrd_gpio,GPIO.LOW)
        status=1
        sw=0
        time.sleep(0.5)

while True:
    power(SW,LED,status)
