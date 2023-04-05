import RPi.GPIO as GPIO
import math
import time

GPIO.setwarnings(False)

BIT_DEPTH = 8
dac = [26, 19, 13, 6, 5 , 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(elem) for elem in bin(value)[2:].zfill(BIT_DEPTH)]

def num2dec(val):
    signal = dec2bin(val)
    GPIO.output(dac, signal)
    return signal

def adc():
    for i in range(1<<BIT_DEPTH):
        x = dec2bin(i)
        print(x)
        #GPIO.output(dac, x)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            GPIO.output(dac, 0)
            return i

def new_adc():
    val = 0
    x = 256
    for i in range(BIT_DEPTH):
        print(x)
        # y = dec2bin(x)
        #print(y)
        #GPIO.output(dac, y)
        time.sleep(0.001)
        if GPIO.input(comp) == 1:
            val += x 
        else:
            val &= ~x
        if x != 2:
            x = x >> 1 
        else:
            x = 1
    return val

try:
    while (True):
        print(new_adc() * 3.3 / (1<<BIT_DEPTH))


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
