import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import serial

from time import sleep

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class state:
	current = 0
	old_x = 0
	old_y = 0

class SampleListener(Leap.Listener):
	"""docstring for SampleListener"""
	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
	
	def on_frame(self, controller):
		frame = controller.frame()
		hand = frame.hands.rightmost
		
		hpx = int(hand.palm_position[0])
		hpy = int(hand.direction[1]*100)
		#print hpx, hpy
		if (state.current == 1 and (state.old_x != hpx or state.old_y != hpy)):
			state.ser.write(str(hpy) + ' ' + str(hpx))
			print state.ser.readline()
		state.old_x = hpx
		state.old_y = hpy

def main():
	listener = SampleListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	
	try:
		state.ser = serial.Serial(port = '/dev/tty.usbmodem1421', baudrate=115200, timeout=10)
	except NameError:
		raise Exception("No Arduino Found")
	
	if state.ser.isOpen():
		state.ser.close()
	state.ser.open()
	
	while True:
		line = state.ser.readline()
		if 'done initializing' in line:
			print line
			break
	
	state.ser.write(str(0) + ' ' + str(0))
	print state.ser.readline()
	state.current = 1
	
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == '__main__':
	main()