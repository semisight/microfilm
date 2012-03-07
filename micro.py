#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, url_for, session, request, g, \
				redirect, flash
from flaskext.oauth import OAuth

from calendar import timegm
import os, datetime

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

##Conventions I will be using:
#g.user is the oauth access token
#access_token is the key (for dicts) that I will be using to store the
#access token under.

####Load from cookie

@app.before_request
def before_request():
	g.user = None
	if 'access_token' in session:
		g.user = session['access_token']

####Views

@app.route('/')
def index():
	name = None

	if g.user is not None:
		resp = facebook.get('/me')
		if resp.status == 200:
			name = resp.data['name']
		else:
			flash('Unable to get name.')

	return render_template('index.html', name=name)

@app.route('/login')
def login():
	return facebook.authorize(callback=url_for('authorized',
        	next=request.args.get('next') or request.referrer or None,
        	_external=True))

@app.route('/logout')
def logout():
	session.pop('access_token', None)
	g.user = None

	return redirect(url_for('index'))

@app.route('/authorized')
@facebook.authorized_handler
def authorized(resp):
	next_url = request.args.get('next') or url_for('index')
	
	if resp is None:
		flash('You need to allow us to pull your data!')
		return redirect(next_url)

	g.user = resp['access_token']
	session['access_token'] = g.user

	return redirect(next_url)

@app.route('/<int:month>/<int:day>/<int:year>')
def display(month, day, year):
	if g.user is None:
		flash('You need to log in to be able to view past feeds!')
		return redirect(url_for('index'))

	#dates to encode into query string
	date_begin = (year, month, day, 0, 0, 0)
	date_end = (year, month, day, 23, 59, 59)

	dates = {'since=': timegm(date_begin),
			 'until=': timegm(date_end)}

	#dates = 'until=time'

	resp = facebook.get('/me/home', data=dates)

	if resp is None or resp.status != 200:
		flash('Can\'t access your news feed!')
		return redirect(url_for('login'))

	date = str(datetime.date.fromtimestamp(timegm(date_begin)))

	return render_template('result.html', posts=resp.data['data'], date=date)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

####Non-view handlers
@facebook.tokengetter
def get_fb_token():
	return g.user, ''

if __name__=='__main__':
	#Set up for Heroku
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
