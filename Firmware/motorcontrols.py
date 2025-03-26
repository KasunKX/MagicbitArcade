from machine import Pin, PWM
import time


a = PWM(Pin(16), freq=500, duty=0)
b = PWM(Pin(17), freq=500, duty=0)
c = PWM(Pin(18), freq=500, duty=0)
d = PWM(Pin(27), freq=500, duty=0)

def directControls(dirc, speed):
        
    if (dirc == 'fwd'):
        a.duty(1)
        b.duty(speed)
        c.duty(speed)
        d.duty(0)
        time.sleep(0.1)
    
    elif (dirc == 'bwd'):
        a.duty(speed)
        b.duty(0)
        c.duty(0)
        d.duty(speed)
        time.sleep(0.1)
    
    elif (dirc == 'lft'):
        a.duty(speed)
        b.duty(0)
        c.duty(speed) # right fwd
        d.duty(0)
        time.sleep(0.1)
    
    elif (dirc == 'rgt'):
        a.duty(0)
        b.duty(speed) # left fwd
        c.duty(0)
        d.duty(speed)
        time.sleep(0.1)
    
    elif (dirc == 'stp'):
        a.duty(0)
        b.duty(0)
        c.duty(0)
        d.duty(0)
    elif (dirc == 'rev'):
        a.duty(speed)
        b.duty(1)
        c.duty(1)
        d.duty(speed)
    

