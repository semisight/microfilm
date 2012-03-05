#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, url_for, sessions, request, g, redirect
import fbconsole

import os

app = Flask(__name__)

###Views

#Ok, let's see... We need to integrate some Graph API in here. I may
#not get around to Twitter by Tuesday. I need to look into a pythonic
#replacement for PHP's strtotime(), then use that to request the
#correct wall posts/news feed for the date entered.
#
#All in all, not bad for a day's hacking.

#Note to self: remove fbconsole. Not suited for more than one user at a
#time :(.

#Login to Facebook and Twitter
@app.route('/')
def index():
	#If login is correct, should redirect to display()
	return render_template('index.html')

@app.route('/login')
def login():
	fbconsole.AUTH_SCOPE = ['read_stream']
	fbconsole.authenticate()

	return str(fbconsole.get('/me/feed'))

@app.route('/<name>')
def hi(name):
	return render_template('result.html', name=name)

@app.route('/<_>/<month>/<day>/<year>')
def display(_, month, day, year):
	return "Stella is estudpido!"

if __name__=='__main__':
	#Set up for Heroku
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
