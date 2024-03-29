import numpy as np
import cv2
import serial as ser
import os
from time import sleep
import time
import RPi.GPIO as GPIO

def set_state(direction, state, pwm, pwm_signal):
    data = "{},{},{},{}\r".format(direction, state, pwm, pwm_signal)
    s.write(data.encode())
    s.flush()

def moveforward():
    state = "0"
    pwm_signal = "25"
    direction = "1"
    pwm = "1"
    set_state(direction, state, pwm, pwm_signal)
    direction = "2"
    pwm = "2"
    set_state(direction, state, pwm, pwm_signal)
    
def movebackward():
    state = "1"
    pwm_signal = "25"
    direction = "1"
    pwm = "1"
    set_state(direction, state, pwm, pwm_signal)
    direction = "2"
    pwm = "2"
    set_state(direction, state, pwm, pwm_signal)

def moveright():
    state = "1"
    pwm_signal = "20"
    direction = "1"
    pwm = "1"
    set_state(direction, state, pwm, pwm_signal)
    state = "0"
    pwm_signal = "20"
    direction = "2"
    pwm = "2"
    set_state(direction, state, pwm, pwm_signal)

def moveleft():
    state = "0"
    pwm_signal = "20"
    direction = "1"
    pwm = "1"
    set_state(direction, state, pwm, pwm_signal)
    state = "1"
    pwm_signal = "20"
    direction = "2"
    pwm = "2"
    set_state(direction, state, pwm, pwm_signal)

def motorstop():
    state = "0"
    pwm_signal = "0"
    direction = "1"
    pwm = "1"
    set_state(direction, state, pwm, pwm_signal)
    state = "1"
    pwm_signal = "0"
    direction = "2"
    pwm = "2"
    set_state(direction, state, pwm, pwm_signal)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
   
if __name__ == "__main__":
   
    port = '/dev/ttyACM0'
    #Serial object for communication with Arduino
    s = ser.Serial(port,9600,timeout=5)

    np.framerate = 15
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
     
    #set GPIO Pins
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    #Capture from external USB webcam instead of the in-built webcam
    cap = cv2.VideoCapture(0)

    #kernel window for morphological operations
    kernel = np.ones((5,5),np.uint8)

    #resize the capture window to 640 x 480
    ret = cap.set(3,640)
    ret = cap.set(4,480)

    #begin capture
    while(True):
        ret, frame = cap.read()

        dist = distance()
        
        #Smooth the frame
        #frame = cv2.GaussianBlur(frame,(11,11),0)

        #Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Mask to extract just the yellow pixels
        #mask = cv2.inRange(hsv,lower_yellow,upper_yellow)

        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv,lower_red,upper_red)
        
        # Range for upper range
        
        # Range for lower red
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        
        mask2 = cv2.inRange(hsv,lower_red,upper_red)
         
        # Generating the final mask to detect red color
        mask = mask1+mask2

        #morphological opening
        #mask = cv2.erode(mask,kernel,iterations=1)
        #mask = cv2.dilate(mask,kernel,iterations=1)

        #morphological closing
        #mask = cv2.dilate(mask,kernel,iterations=1)
        #mask = cv2.erode(mask,kernel,iterations=1)

        #Detect contours from the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        if(len(cnts) > 0):
            #Contour with greatest area
            c = max(cnts,key=cv2.contourArea)
            #Radius and center pixel coordinate of the largest contour
            ((x,y),radius) = cv2.minEnclosingCircle(c)

            if radius > 5:
                #Draw an enclosing circle
                cv2.circle(frame,(int(x), int(y)), int(radius),(0, 255, 255), 2)

                #Draw a line from the center of the frame to the center of the contour
                cv2.line(frame,(320,240),(int(x), int(y)),(0, 0, 255), 1)
                #Reference line
                cv2.line(frame,(320,0),(320,480),(0,255,0),1)

                radius = int(radius)

                #distance of the 'x' coordinate from the center of the frame
                #wdith of frame is 640, hence 320
                length = 320-(int(x))

                if dist < 75:#motorstop
                        motorstop()
                        print('stop -- ',length,dist)

                elif length > 250:#turn left
                        moveleft()
                        print('left -- ',length,dist)
                        
                elif length < -250:#turn right
                        moveright()
                        print('right -- ', length,dist)

                elif length < 250 or length >-250:#move forward
                        moveforward()
                        print('forward -- ', length,dist)
                else :
                    motorstop()
                    sleep(0.01)

            else:
              motorstop()
              sleep(0.01)


        #display the image
        cv2.imshow('frame',frame)
        #Mask image
        cv2.imshow('mask',mask)
        #Quit if user presses 'q'
        if cv2.waitKey(15) & 0xFF == ord('q'):
            motorstop()
            break

    #Release the capture
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup();
