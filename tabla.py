import serial as ser
import bluetooth
#from colour_follow.py import colour_track()
import numpy as np
import cv2
import os
from time import sleep
	
def set_state(direction, state, pwm, pwm_signal):
    data = "{},{},{},{}\r".format(direction, state, pwm, pwm_signal)
    s.write(data.encode())
    s.flush()

def main_input():
		print("Please select a mode")
		
		recvdata = client_sock.recv(1024)
		recv = recvdata
		
		if recv == '1':
			mode1()
		
		elif recv == '2':
			mode2()

		elif recv == '3':
			mode3()
		
		elif recv == 'q':
			print ("Quitting program")	
			quit_()
			
def mode1():
        
	check = '0'
        print('mode1')
        
	while(check!= 'q'):
                recvdata = client_sock.recv(1024)
                check = recvdata
                
                if check == 'f':   
                        moveforward()

                elif check =='b':
                        movebackward()

                elif check =='r':
                        moveright()

                elif check =='l':
                        moveleft()

        motorstop()        
        print("Back to Main Menu")
	

def mode2():
        
        print('mode2')
        mode2_var = '0'

        while(mode2_var!= 'q'):
                #Capture from external USB webcam instead of the in-built webcam (shitty quality)
                cap = cv2.VideoCapture(0)

                #kernel window for morphological operations
                kernel = np.ones((5,5),np.uint8)

                #resize the capture window to 640 x 480
                ret = cap.set(3,640)
                ret = cap.set(4,480)

                #upper and lower limits for the color yellow in HSV color space
                lower_yellow = np.array([20,100,100])
                upper_yellow = np.array([30,255,255])

                #begin capture
                while(True):
                    recvdata = client_sock.recv(1024)
                    mode2_var = recvdata
                
                    ret, frame = cap.read()

                    #Smooth the frame
                    frame = cv2.GaussianBlur(frame,(11,11),0)

                    #Convert to HSV color space
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    #Mask to extract just the yellow pixels
                    mask = cv2.inRange(hsv,lower_yellow,upper_yellow)

                    #morphological opening
                    mask = cv2.erode(mask,kernel,iterations=2)
                    mask = cv2.dilate(mask,kernel,iterations=2)

                    #morphological closing
                    mask = cv2.dilate(mask,kernel,iterations=2)
                    mask = cv2.erode(mask,kernel,iterations=2)

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

                            if length > 150:#turn left
                                    moveleft()
                                    print('left')
                                    
                            elif length < -150:#turn right
                                    moveright()
                                    print('right')

                            elif length <150 or length >-150:#move forward
                                    moveforward()
                                    print('forward')

                            else:
                                    motorstop()
                                    print('stop')
                                    sleep(0.01)

                        else:
                            motorstop()
                            sleep(0.01)

                        if mode2_var == 'q':
                                break


                    #display the image
                    cv2.imshow('frame',frame)
                    #Mask image
                    cv2.imshow('mask',mask)
            
        motorstop()
        #Release the capture
        cap.release()
        cv2.destroyAllWindows()
          
                	
def mode3():
	print("Mode 3")
	input()
	
def quit_():
	print("quitting program")
	direction = "1"
	state = "1"
	pwm = "1"
	pwm_signal = "0"
	set_state(direction, state, pwm, pwm_signal)
	direction = "2"
	state = "1"
	pwm = "2"
	pwm_signal = "0"
	set_state(direction, state, pwm, pwm_signal)
	server_sock.close()
	
	sys.exit()
	
def moveforward():
        print ("forward")
        state = "0"
	pwm_signal = "15"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	direction = "2"
	pwm = "2"
	set_state(direction, state, pwm, pwm_signal)
	

def movebackward():
        print ("backward")
        state = "1"
	pwm_signal = "15"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	direction = "2"
	pwm = "2"
	set_state(direction, state, pwm, pwm_signal)
	

def moveright():
        print ("right")
        state = "1"
	pwm_signal = "15"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	state = "0"
	pwm_signal = "15"
	direction = "2"
	pwm = "2"
	set_state(direction, state, pwm, pwm_signal)


def moveleft():
        print ("left")
        state = "0"
	pwm_signal = "15"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	state = "1"
	pwm_signal = "15"
	direction = "2"
	pwm = "2"
	set_state(direction, state, pwm, pwm_signal)


def motorstop():
        print ("stop")
        direction = "1"
	state = "1"
	pwm = "1"
	pwm_signal = "0"
	set_state(direction, state, pwm, pwm_signal)
	direction = "2"
	state = "1"
	pwm = "2"
	pwm_signal = "0"
	set_state(direction, state, pwm, pwm_signal)

if __name__ == "__main__":
        print("waiting for connection in main")
	port = '/dev/ttyACM0'
        s = ser.Serial(port,9600,timeout=5)
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	port = 1
	server_sock.bind(("",port))
	server_sock.listen(1)
	client_sock,address = server_sock.accept()
	print("accepted connection from ", address)
	
	while True:
		main_input()
