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
        self.debug("Client connected")
        ID = self.get_address()
	self.queue.put({'type':'open', 'ID': ID, 'socket': self})

    def on_message(self, message):
        self.debug("Message recieved: {}".format(message))
	self.queue.put({'type':'response', 'value': message})

    def on_close(self):
        self.debug("Client closed connection")
	address = self.request.connection.context.address
	ID = address[0]+':'+str(address[1])
	self.queue.put({'type':'close', 'ID': ID})

class Server(Thread):
    def __init__(self, port, queue, debug=False):
	Thread.__init__(self)
	self.port = port
	self.logger = Logger("server:{}".format(port))
	self.debug = debug
	self.queue = queue

    def run(self):
	self.logger.info("Starting up...")
        app = web.Application([(r'/ws', WsRequestHandler, {'queue': self.queue, 'logger': self.logger, 'debug': self.debug})])
        app.listen(self.port)
        ioloop.IOLoop.instance().start()

