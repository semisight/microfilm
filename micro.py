from __future__ import division
from flask import Flask

app = Flask(__name__)

###Views
@app.route('/')
def index():
	pass

@app.route('/<name>')
def hi(name):
	return 'hi, {0}!'.format(name)

if __name__=='__main__':
	app.run()
