#!/usr/bin/python
# coding: utf-8; -*-

import RPi.GPIO as GPIO
import time, signal

import send_ref
url_count = 'http://192.168.1.89:8000/cgi-bin/app.py'
url_flag = 'http://192.168.1.89:8000/cgi-bin/app.py'


REF_PIN=24

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(REF_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

counter = 0

def event_callback(gpio_pin):
    global counter
    counter = counter + 1

GPIO.add_event_detect(REF_PIN,GPIO.RISING,
                        callback=event_callback,bouncetime=10)


sigtime = 1

def handler(signum, frame):
    global counter
    params = {
              'count' : counter,
              }
    try:
        send_ref.send_ref(url_count,params)
    except:
        pass
    print params
    counter = 0
    signal.alarm(sigtime)

signal.signal(signal.SIGALRM, handler)

signal.alarm(sigtime)



SW = 26
LED = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW,GPIO.IN)
#GPIO.setup(SW,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED,GPIO.OUT)
status = False

"""
def event_callback_flag(gpio_pin):
    global status
    if status == False:
        status = True
        GPIO.output(LED,GPIO.LOW)
    elif status == True:
        status = False
        GPIO.output(LED,GPIO.HIGH)
    print(status)

GPIO.add_event_detect(SW,GPIO.RISING,
                        callback=event_callback_flag,bouncetime=1000)
"""

def power(sw_gpio,led_gpio):
    global status
    sw = GPIO.input(sw_gpio)
    if sw:
        if status == False:	
            GPIO.output(led_gpio,GPIO.LOW)
            status = True
            params = {
                      'flag'  : status,
                     }
            try:
                send_ref.send_ref(url_flag,params)
            except:
                pass
            print(status)
            time.sleep(0.2)
        elif status == True:
            GPIO.output(led_gpio,GPIO.HIGH)
            status = False
            params = {
                      'flag'  : status,
                     }
            try:
                send_ref.send_ref(url_flag,params)
            except:
                pass
            print(status)
            time.sleep(0.2)
"""
    if sw:
        params = {
                  'flag'  : status,
                 }
        try:
            send_ref.send_ref(url_flag,params)
        except:
            pass
#        print(status)
"""



RIGHT = 05
LEFT = 06
GPIO.setmode(GPIO.BCM)
GPIO.setup(RIGHT,GPIO.IN)
GPIO.setup(LEFT,GPIO.IN)
#GPIO.setup(RIGHT,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(LEFT,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
angle = 0

"""
def angle_right(gpio_pin):
    global angle
    angle += 15
    if angle == 360:
        angle = 0

def angle_left(gpio_pin):
    global angle
    angle -= 15
    if angle == -360:
        angle = 0

GPIO.add_event_detect(RIGHT,GPIO.RISING,
                        callback=angle_right,bouncetime=500)
GPIO.add_event_detect(LEFT,GPIO.RISING,
                        callback=angle_left,bouncetime=500)
"""
def turn(right_gpio,left_gpio):
    global angle
    right = GPIO.input(right_gpio)
    left = GPIO.input(left_gpio)
    if right:
        angle = 15
        params = {'angle' : angle}
        try:
            send_ref.send_ref(url_angle,params)
        except:
            pass
        print(angle)
        angle = 0
        time.sleep(0.2)
    elif left:
        angle = -15
        params = {'angle' : angle}
        try:
            send_ref.send_ref(url_angle,params)
        except:
            pass
        print(angle)
        angle = 0
        time.sleep(0.2)

try:
    while True: 
        power(SW,LED)
        turn(RIGHT,LEFT)
        continue
except KeyboardInterrupt:
    signal.alarm(0)
    GPIO.cleanup()
