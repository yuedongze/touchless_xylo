import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import requests

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
		info = {'azim':hpy, 'elev':hpx}
		if (state.old_x != hpx or state.old_y != hpy):
			res = requests.post('http://192.168.11.138:5000', json=info)
		sleep(0.01)
		state.old_x = hpx
		state.old_y = hpy

def main():
	listener = SampleListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == '__main__':
	main()