import serial as ser
import bluetooth

import os

def main():
        print("waiting for connection in main")
	port = '/dev/ttyACM0'
        s = ser.Serial(port,9600,timeout=5)
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	port = 2
	server_sock.bind(("",port))
	server_sock.listen(1)
	client_sock.address = server_sock.accept()
	print("accepted connection from ", address)
	
	while True:
		input_()
	
def set_state(direction, state, pwm, pwm_signal):
    data = "{},{},{},{}\r".format(direction, state, pwm, pwm_signal)
    s.write(data.encode())
    s.flush()

def input_():
		print("Please select a mode")
		
		recvdata = client_sock.recv(1024)
		check = recvdata
		
		if check == '1':
			mode1()
		
		elif check == '2':
			mode2()

		elif check == '3':
			mode3()
		
		elif check == 'q':
			print "Quitting program"	
			quit_()
			
def mode1():
	if check == 'f':   
		state = "0"
		pwm_signal = "15"
		direction = "1"
		pwm = "1"
		set_state(direction, state, pwm, pwm_signal)
		direction = "2"
		pwm = "2"
		set_state(direction, state, pwm, pwm_signal)

	elif check =='b':
		state = "1"
		pwm_signal = "15"
		direction = "1"
		pwm = "1"
		set_state(direction, state, pwm, pwm_signal)
		direction = "2"
		pwm = "2"
		set_state(direction, state, pwm, pwm_signal)

	elif check =='r':
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

	elif check =='l':
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
 
	elif check == 'q':
		print("Back to Main Menu")
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
		input()

def mode2():
	print("Mode 2")
	input()
	
	
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

if __name__ == '__main__':
    main()
