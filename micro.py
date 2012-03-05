#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, url_for, sessions, request, g, redirect
from flaskext.oauth import OAuth

import os

#setup code
app = Flask(__name__)
app.secret_key = 'pagerduty'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='187344811378870',
    consumer_secret='7f75c822a976c064f479e4fe93c68d9d',
    request_token_params={'scope': 'read_stream'}
)

###Views

#Ok, let's see... We need to integrate some Graph API in here. I may
#not get around to Twitter by Tuesday. I need to look into a pythonic
#replacement for PHP's strtotime(), then use that to request the
#correct wall posts/news feed for the date entered.
#
#All in all, not bad for a day's hacking.

#Note to self: remove fbconsole. Not suited for more than one user at a
#time :(.

#If you're logged in, you should get here
@app.route('/')
@facebook.authorized_handler
def index(resp):
	if resp == None:
		#if not logged in, redirect to /login.
		return redirect(url_for('greetings'))

	me = str(facebook.get('/me'))
	return render_template('index.html', me=me)

@app.route('/login')
def login():
	return facebook.authorize(callback = url_for('index',
								next = request.args.get('next') or
								request.referrer or None,
								_external = True))

@app.route('/about')
def greetings():
	return render_template('index.html')

@app.route('/<month>/<day>/<year>')
def display(month, day, year):
	return "Stella is estudpido!"

if __name__=='__main__':
	#Set up for Heroku
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
