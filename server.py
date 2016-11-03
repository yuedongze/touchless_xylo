from flask import Flask, request
import serial
import subprocess
from time import sleep
app = Flask(__name__)

class state:
	ser = 0

@app.route('/', methods=['GET','POST'])
def pyhandler():
	content = request.json
	hpy = content['elev']
	hpx = content['azim']
	state.ser.write(str(hpy) + ' ' + str(hpx))
	print state.ser.readline()
	return '''content'''

if __name__ == '__main__':
	
	port = subprocess.check_output("dmesg | grep 'cdc_acm 1-1.2' | tail -1", shell=True).split(':')
	if port == ['']:
		raise Exception("NO DEV")
	port = '/dev/'+port[2].strip()
	print port
	try:
		state.ser = serial.Serial(port, baudrate=115200, timeout=10)
	except NameError:
		raise Exception("ERR")
	
	if state.ser.isOpen():
		state.ser.close()
	state.ser.open()

	while True:
		line = state.ser.readline()
		if 'done initializing' in line:
			print line
			break
	
	app.run(host='0.0.0.0')
