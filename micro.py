#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, url_for

import os

app = Flask(__name__)

###Views

#Login to facebook and Twitter
@app.route('/')
def index():
	#If login is correct, should redirect to display()
	return render_template('index.html')

@app.route('/<name>')
def hi(name):
	return render_template('result.html', name=name)

@app.route('/<_>/<month>/<day>/<year>')
def display(_, month, day, year):
	return "Stella is estudpido!"

if __name__=='__main__':
	#Set up for Heroku
	#note: may need set port num to env variable PORT (default:5000)
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', debug=True)
