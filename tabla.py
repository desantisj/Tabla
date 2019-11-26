import serial as ser
import bluetooth
import numpy as np
from imutils.video import VideoStream
import imutils
import RPi.GPIO as GPIO
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
        print('Mode 1')
        
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
            # construct the argument parse and parse the arguments
            ap = argparse.ArgumentParser()
            ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
            ap.add_argument("-b", "--buffer", type=int, default=32,
                    help="max buffer size")
            args = vars(ap.parse_args())

            # initialize the list of tracked points, the frame counter,
            # and the coordinate deltas
            pts = deque(maxlen=args["buffer"])
            counter = 0
            (dX, dY) = (0, 0)
            direction = ""

            # if a video path was not supplied, grab the reference
            # to the webcam
            if not args.get("video", False):
                    vs = VideoStream(src=0).start()

            # otherwise, grab a reference to the video file
            else:
                    vs = cv2.VideoCapture(args["video"])

            # allow the camera or video file to warm up
            time.sleep(2.0)

            # keep looping
            while True:
                    mode2_var = client_sock.recv(1024)
                    
                    dist = distance()
                    
                    # grab the current frame
                    frame = vs.read()

                    # handle the frame from VideoCapture or VideoStream
                    frame = frame[1] if args.get("video", False) else frame

                    # if we are viewing a video and we did not grab a frame,
                    # then we have reached the end of the video
                    if frame is None:
                            break

                    # resize the frame, blur it, and convert it to the HSV
                    # color space
                    frame = imutils.resize(frame, width=600)
                    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                    # construct a mask for the color "green", then perform
                    # a series of dilations and erosions to remove any small
                    # blobs left in the mask
                    
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
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)

                    # find contours in the mask and initialize the current
                    # (x, y) center of the ball
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)
                    center = None

                    # only proceed if at least one contour was found
                    if len(cnts) > 0:
                            # find the largest contour in the mask, then use
                            # it to compute the minimum enclosing circle and
                            # centroid
                            c = max(cnts, key=cv2.contourArea)
                            ((x, y), radius) = cv2.minEnclosingCircle(c)
                            M = cv2.moments(c)
                            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                            # only proceed if the radius meets a minimum size
                            if radius > 10:
                                    # draw the circle and centroid on the frame,
                                    # then update the list of tracked points
                                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                            #Draw a line from the center of the frame to the center of the contour
                            cv2.line(frame,(300,300),(int(x), int(y)),(0, 0, 255), 1)
                            #Reference line
                            cv2.line(frame,(300,0),(300,600),(0,255,0),1)

                            radius = int(radius)

                            #distance of the 'x' coordinate from the center of the frame
                            #wdith of frame is 640, hence 320
                            length = 300-(int(x))

                            if dist < 75:
                                    motorstop()
                                    print('stop -- ', length, dist)

                            elif length > 200:#turn left
                                    moveleft()
                                    print('left -- ',length)
                                    
                            elif length < -200:#turn right
                                    moveright()
                                    print('right -- ', length)

                            elif length <= 200 and length >= -200:
                            #move forward
                                    moveforward()
                                    print('forward -- ', length)

                            else :
                                print("stop1")
                                motorstop()
                                sleep(0.01)


            ##	# show the frame to our screen and increment the frame counter
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

            # if we are not using a video file, stop the camera video stream
            if not args.get("video", False):
                    vs.stop()

            # otherwise, release the camera
            else:
                    vs.release()
            
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
	GPIO.cleanup()
	
	sys.exit()
	
def moveforward():
        print("forward")
        state = "0"
        pwm_signal = "35"
        direction = "1"
        pwm = "1"
        set_state(direction, state, pwm, pwm_signal)
        state = "0"
        pwm_signal = "28"
        direction = "2"
        pwm = "2"
        set_state(direction, state, pwm, pwm_signal)
	

def movebackward():
        print("backward")
        state = "1"
        pwm_signal = "35"
        direction = "1"
        pwm = "1"
        set_state(direction, state, pwm, pwm_signal)
        state = "1"
        pwm_signal = "28"
        direction = "2"
        pwm = "2"
        set_state(direction, state, pwm, pwm_signal)
	

def moveright():
        print ("right")
        state = "1"
	pwm_signal = "22"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	state = "0"
	pwm_signal = "22"
	direction = "2"
	pwm = "2"
	set_state(direction, state, pwm, pwm_signal)


def moveleft():
        print ("left")
        state = "0"
	pwm_signal = "22"
	direction = "1"
	pwm = "1"
	set_state(direction, state, pwm, pwm_signal)
	state = "1"
	pwm_signal = "22"
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

def distacne():
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
        print("waiting for connection in main")
	port = '/dev/ttyACM0'
        s = ser.Serial(port,9600,timeout=5)

        GPIO.setmode(GPIO.BCM)

        #set GPIO Pins
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24

        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
    
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	port = 1
	server_sock.bind(("",port))
	server_sock.listen(1)
	client_sock,address = server_sock.accept()
	print("accepted connection from ", address)
	
	while True:
		main_input()
