#This code was taken from flask.pocoo.org. All credit goes to the
#developer of Flask. He is really awesome in general.

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from micro import app

import os

#Heroku will give the app different port values through PORT,
#so we need the os.environ...
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(int(os.environ.get('PORT', 5000)))
IOLoop.instance().start()
