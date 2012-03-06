#This code was taken from flask.pocoo.org. All credit goes to the
#developer of Flask. He is really awesome in general.

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from micro import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()
