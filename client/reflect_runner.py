#!/usr/bin/python
# coding: utf-8; -*-

import RPi.GPIO as GPIO
import time, signal


REF_PIN=21

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(REF_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

counter = 0

def event_callback(gpio_pin):
    global counter
    counter = counter + 1

GPIO.add_event_detect(REF_PIN,GPIO.RISING,
                        callback=event_callback,bouncetime=10)


#import power_count

SW = 26
LED = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
num = 0
status = False

def power(sw_gpio,led_gpio):
    global num
    global status
    sw = GPIO.input(sw_gpio)
    if sw:
        num += 1
        print(num)
    if num %2 == 0:
        GPIO.output(led_gpio,GPIO.HIGH)
        status = False
        time.sleep(0.2)
    if num %2 == 1:
        GPIO.output(led_gpio,GPIO.LOW)
        status = True
        time.sleep(0.2)


import send_ref
url    = 'http://192.168.1.89:8000/cgi-bin/app.py'


sigtime = 1

def handler(signum, frame):
    global counter
    global status
    params = {
              'count' : counter,
              'flag'  : status,
              }
    try:
        send_ref.send_ref(url,params)
    except:
        pass
    print params
    counter = 0
    signal.alarm(sigtime)

signal.signal(signal.SIGALRM, handler)

signal.alarm(sigtime)


try:
    while True: 
        power(SW,LED)
        continue
except KeyboardInterrupt:
    signal.alarm(0)
    GPIO.cleanup()
