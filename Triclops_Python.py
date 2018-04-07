#This is the file for our python code. I'm sure thats what we'll start with. If not, then I owe everyone a high-five!
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
Step = 15
DIR = 13
Enable = 36
Rotate_1Switch = 40
Rotate_2Switch = 38
Rotate_3KillSwitch = 32
GPIO.setup(Step, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

##Switch Setup
GPIO.setup(Rotate_1Switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Rotate_2Switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Rotate_3KillSwitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)

##Move one direction
GPIO.output(DIR, False)
for i in range(800):
    GPIO.output(Step, True)
    GPIO.output(Step, False)
    time.sleep(0.001)
    
##Move one direction
GPIO.output(DIR, True)
for i in range(800):
    GPIO.output(Step, True)
    GPIO.output(Step, False)
    time.sleep(0.001)

DIRBool = True
clockwise = True
counterClockwise = False
whileFlag = True
while True:
    input_state = GPIO.input(Rotate_1Switch)
    #print(input_state)
    clockWiseFlag = True
    if (input_state == False):
        while (clockWiseFlag):
            #print("button pressed")
            GPIO.output(DIR, counterClockwise)
            GPIO.output(Step, True)
            GPIO.output(Step, False)
            time.sleep(0.001)
            input_state = GPIO.input(Rotate_1Switch)
            input_state3 = GPIO.input(Rotate_3KillSwitch)
            if (input_state3 == False):
                clockWiseFlag = False
    input_state2 = GPIO.input(Rotate_2Switch)
    #print(input_state2)
    counterClockWiseFlag = True
    if (input_state2 == False):
        while (counterClockWiseFlag):
            #DIRBool = not(DIRBool)
            GPIO.output(DIR, clockwise)
            GPIO.output(Step, True)
            GPIO.output(Step, False)
            time.sleep(0.001)
            input_state = GPIO.input(Rotate_1Switch)
            input_state3 = GPIO.input(Rotate_3KillSwitch)
            if (input_state3 == False):
                counterClockWiseFlag = False

##    input_state3 = GPIO.input(Rotate_3KillSwitch)
##    if (input_state3 == False):
##        whileFlag = False
##        
        
        
