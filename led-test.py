import RPi.GPIO as GPIO
from contextlib import contextmanager
from time import sleep

# Pin numbers
# Color value for first of row pair
R1 = 17
G1 = 18
B1 = 22
RGB1 = (R1, G1, B1)

# Color value for second of row pair
R2 = 23
G2 = 24
B2 = 25
RGB2 = (R2, G2, B2)

# A, B, C, D pins set the current row pair, n and n + 16
A = 7
B = 8
C = 9
D = 10

# Fuckery
OE_MINUS = 2
# Changes voltages up and down to move through columns of the board
CLOCK = 3
# After 64 clock cycles, set to high to move RBG values to somewhere magical
# and allow clock to restart
LATCH = 4


@contextmanager
def gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(G1, GPIO.OUT)
    GPIO.setup(B1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(G2, GPIO.OUT)
    GPIO.setup(B2, GPIO.OUT)

    GPIO.setup(A, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    GPIO.setup(C, GPIO.OUT)
    GPIO.setup(D, GPIO.OUT)

    GPIO.setup(OE_MINUS, GPIO.OUT)
    GPIO.setup(CLOCK, GPIO.OUT)
    GPIO.setup(LATCH, GPIO.OUT)

    try:
        yield
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()

def setRGB((rValue, gValue, bValue), (rPin, gPin, bPin)):
    ''' values are either 1 or 0, indicating high or low'''
    rVoltage = GPIO.HIGH  if rValue == 1 else  GPIO.LOW
    gVoltage = GPIO.HIGH  if gValue == 1 else  GPIO.LOW
    bVoltage = GPIO.HIGH  if bValue == 1 else  GPIO.LOW

    GPIO.output(rPin, rVoltage)
    GPIO.output(gPin, gVoltage)
    GPIO.output(bPin, bVoltage)

def setCurrentRowPair(rowNum):
    ''' sets current row pair to rowNum and rowNum + 16'''
    aVoltage = GPIO.HIGH if (rowNum & 0b0001)  else GPIO.LOW
    bVoltage = GPIO.HIGH if (rowNum & 0b0010) else GPIO.LOW
    cVoltage = GPIO.HIGH if (rowNum & 0b0100) else GPIO.LOW
    dVoltage = GPIO.HIGH if (rowNum & 0b1000) else GPIO.LOW

    GPIO.output(A, aVoltage)
    GPIO.output(B, bVoltage)
    #GPIO.output(A, GPIO.HIGH)
    #GPIO.output(B, GPIO.HIGH)
    GPIO.output(C, cVoltage)
    GPIO.output(D, dVoltage)

def pulseClock():
    GPIO.output(CLOCK, GPIO.HIGH)
    #sleep(.5)
    GPIO.output(CLOCK, GPIO.LOW)

def setLatch(value):
    latchVal = GPIO.HIGH if value == 1 else GPIO.LOW
    GPIO.output(LATCH, latchVal)


def setToZero():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(G1, GPIO.LOW)
    GPIO.output(B1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)
    GPIO.output(G2, GPIO.LOW)
    GPIO.output(B2, GPIO.LOW)

    GPIO.output(A, GPIO.LOW)
    GPIO.output(B, GPIO.LOW)
    GPIO.output(C, GPIO.LOW)
    GPIO.output(D, GPIO.LOW)

    GPIO.output(OE_MINUS, GPIO.LOW)
    GPIO.output(CLOCK, GPIO.LOW)
    GPIO.output(LATCH, GPIO.LOW)



import random
random_duration = lambda: random.choice([0.5, 1, 1.5, 2, 2.5])


with gpio():
    setToZero()
    setCurrentRowPair(5)
    setRGB((1, 1, 0), (R2, G2, B2))
    setRGB((0, 1, 1), (R1, G1, B1))
    
    #GPIO.output(CLOCK, GPIO.HIGH)
    
    for i in range(3):
        pulseClock()

    setLatch(1)
    #pulseClock()
    


    #setLatch(0)

    #setToZero()


    i = 0
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(1,1,1),(0,1,1)]
    c = 0
    while True:
 

        for j in range(300):
            
            setRGB(colors[c], (R1, G1, B1))
            if j % 10 != 0:
                c = 0
            #random_color = random.choice([(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(1,1,1),(0,1,1)])
            setRGB(colors[c], (R2, G2, B2))
            setCurrentRowPair(i) 
            pulseClock()
            i = i + 1
            if i == 16:
                i = 0
            c = c + 1
            if c == 7:
                c = 0

        
        #setCurrentRowPair(random.randint(0,15))
            
        setLatch(1)
        
        setLatch(0)


    sleep(5)

    #sleep(random_duration())
    print "helloooo"
