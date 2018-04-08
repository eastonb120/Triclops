#This is the file for our python code. I'm sure thats what we'll start with. If not, then I owe everyone a high-five!
import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#INITIAL PIN CONFIGURATION
#--------------------------------------------------------------------
#STEP GPIO 22
Step = 15
GPIO.setup(Step, GPIO.OUT)
#--------------------------------------------------------------------
#DIR GPIO 27
DIR = 13
GPIO.setup(DIR, GPIO.OUT)
#--------------------------------------------------------------------
#ENABLE GPIO 16
Enable = 36
#--------------------------------------------------------------------
#clockWise_PIR GPIO 21
clockWise_PIR = 40
#--Push Button Simulation
#GPIO.setup(clockWise_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#--Actual PIR
GPIO.setup(clockWise_PIR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#--------------------------------------------------------------------
#counterClockWise_PIR GPIO 20
counterClockWise_PIR = 38
#--Push Button Simulation
#GPIO.setup(counterClockWise_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#--Actual PIR
GPIO.setup(counterClockWise_PIR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#--------------------------------------------------------------------
#center_PIR GPIO 12
center_PIR = 32

#--Push Button Simulation
#GPIO.setup(center_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#--Actual PIR
GPIO.setup(center_PIR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#--------------------------------------------------------------------

#Define boolean for rotation behavior. Linked to DIR GPIO
clockwise = False
counterClockwise = True


#Rotate Motor Clockwise
GPIO.output(DIR, False)
for i in range(800):
    GPIO.output(Step, True)
    GPIO.output(Step, False)
    time.sleep(0.001)
    
#Rotate Motor Counter Clockwise
GPIO.output(DIR, True)
for i in range(800):
    GPIO.output(Step, True)
    GPIO.output(Step, False)
    time.sleep(0.001)



#Infinite Main Loop (Allows logic to operate until program terminated)
while True:  

    print("Loop Begin")
    #Clockwise Rotation
    #Swap from False to TRUE
    if(GPIO.input(clockWise_PIR) == True):
        
        print("\nClockwise PIR Triggered")
        #Set Rotation Direction to Clockwise
        GPIO.output(DIR, clockwise)
        
        while(True):
            
            #Step in Clockwise Direction
            GPIO.output(Step, True)
            GPIO.output(Step, False)
            time.sleep(0.1)

            #If Center PIR is Triggered, stop stepping and exit to main loop
            if(GPIO.input(center_PIR) == True):
                print("Center PIR Triggered")
                time.sleep(3)
                break


   

    #Counter Clockwise Rotation
    if(GPIO.input(counterClockWise_PIR) == True):
        
        print("\nCounter Clockwise PIR Triggered")
        #Set Rotation Direction to Counter Clockwise
        GPIO.output(DIR, counterClockwise)
        
        while (True):
            
            #Step in Counter Clockwise Direction
            GPIO.output(Step, True)
            GPIO.output(Step, False)
            time.sleep(0.1)

            #If Center PIR is Triggered, stop stepping and exit to main loop
            if (GPIO.input(center_PIR) == True):
                print("Center PIR Triggered")
                time.sleep(3)
                break
            
    print("Sleeping")

    print("Wake up!")
        
        

        
        
