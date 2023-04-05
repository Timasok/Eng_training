import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)


BIT_DEPTH = 8
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24,25,8,7,12,16,20,21]
comp = 4
troyka = 17
levels = 2 ** len(dac)
maxV = 3.3

GPIO.setmode(GPIO.BCM)
for i in dac:
    GPIO.setup(i, GPIO.OUT)
for i in leds:
    GPIO.setup(i, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]


def adc():
    for i in range(256):
        x = dec2bin(i)
        GPIO.output(dac, x)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            GPIO.output(dac, 0)
            return i
    return 256

def new_adc():
    bin = 0

    for i in range(7, -1, -1):
        bin += (1 << i)
        GPIO.output( dac, dec2bin( bin ) )
        time.sleep(0.0005)
        val = GPIO.input( comp )
        
        if val == 0:
            bin -= (1 << i)
    
    return bin


try:
    while (True):
        v = new_adc()
        n = v // 16
        n = min(8, n)
        GPIO.output(leds, [1] * n + [0] * (BIT_DEPTH - n))


finally:
    for i in dac:
        GPIO.output(dac, 0)
    GPIO.cleanup()

