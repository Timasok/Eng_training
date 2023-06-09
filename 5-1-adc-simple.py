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
        GPIO.output(dac, x)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            GPIO.output(dac, 0)
            return i

try:
    while (True):
        print(adc() * 3.3 / (1<<BIT_DEPTH))


finally:

    GPIO.output(dac, 0)
    GPIO.cleanup()
