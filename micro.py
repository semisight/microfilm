#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, url_for

app = Flask(__name__)

###Views

#Login to facebook and Twitter
@app.route('/')
def index():
	#If login is correct, should redirect to display()
	return render_template('index.html')

@app.route('/<name>')
def hi(name):
	return 'hi, {0}!'.format(name)

@app.route('/<_>/<month>/<day>/<year>')
def display(_, month, day, year):
	return "Stella is estudpido!"

if __name__=='__main__':
	app.run(debug=True)
