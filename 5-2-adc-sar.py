import RPi.GPIO as GPIO
import math
import time

GPIO.setwarnings(False)

BIT_DEPTH = 8
dac = [26, 19, 13, 6, 5 , 11, 9, 10]
comp = 4
troyka = 17
EPS = 0.001

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    # if (value - 6.57) < 0.1:
    #     return [0,0,0,0,0,0,0,1]
    return [int(elem) for elem in bin(value%256)[2:].zfill(BIT_DEPTH)]

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

def new_adc( dac, comp ):
    bin = 0

    for i in range(7, -1, -1):
        bin += (1 << i)
        GPIO.output( dac, dec2bin( bin ) )
        time.sleep(0.0005)
        val = GPIO.input( comp )
        
        if val == 0:
            bin -= (1 << i)
    
    return bin

# def new_adc():
#     val = 0
#     arr = [256, 128, 64, 32, 16, 8, 4, 2, 1]
#     for i in arr:
#         y = dec2bin(i)
#         print(y)
#         # GPIO.output(dac, y)
#         time.sleep(0.001)
#         if GPIO.input(comp) == 1:
#             val += i 
#         else:
#             val &= ~i
#     return val

try:
    while (True):
        print(new_adc(dac,comp) * 3.3 / (1<<BIT_DEPTH))


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
