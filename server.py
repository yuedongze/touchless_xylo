from flask import Flask,request,url_for,redirect, url_for, render_template
import os
from time import sleep
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def pyhandler():
	content = request.json
	print content['azim'], content['elev']
	return '''content'''

if __name__ == '__main__':
	app.run(debug=True)