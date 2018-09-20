from threading import Thread
from logging import Logger
from tornado import websocket, web, httpserver, ioloop

class WsRequestHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
	self.queue = kwargs.pop('queue')
	self.logger = kwargs.pop('logger')
	self.dbg = kwargs.pop('debug')
	super(WsRequestHandler, self).__init__(*args, **kwargs)

    def get_address(self):
	address = self.request.connection.context.address
	return address[0]+':'+str(address[1])		
        
    def debug(self, message):
	if self.dbg:
            self.logger.debug("[{}] {}".format(self.get_address(), message))

    def open(self):
        self.logger.info("Client connected")
        ID = self.get_address()
	self.queue.new_client(ID, self)

    def on_message(self, message):
        self.debug("Message recieved: {}".format(message))
        self.queue.new_message(self.get_address(), message)

    def on_close(self):
        self.logger.warn("Client [{}] closed connection".format(self.get_address()))
	self.queue.client_disconnect(self.get_address())

class WebSocketServerThread(Thread):
    def __init__(self, app):
	Thread.__init__(self)
	self.port = app.port
	self.logger = Logger("server:{}".format(self.port))
	self.debug = app.debug
	self.queue = app

    def run(self):
	self.logger.info("Starting up...")
        app = web.Application([(r'/ws', WsRequestHandler, {'queue': self.queue, 'logger': self.logger, 'debug': self.debug})])
        app.listen(self.port)
        ioloop.IOLoop.instance().start()

