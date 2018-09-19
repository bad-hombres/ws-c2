from threading import Thread
from server import WebSocketServerThread
from console import ConsoleThread
from logging import Logger
from Queue import Queue, Empty
import sys

class MainApplicationThread(Thread):
    def __init__(self, port, debug=False):
        Thread.__init__(self)
        self.port = port
        self.debug = debug
        self.logger = Logger("main")
        self._fromWsQueue = Queue(0)
        self._fromConsole = Queue(0)
        self._toConsole   = Queue(0)

    def run(self):
        self.ws = WebSocketServerThread(self)
        self.ws.daemon = True

        self.console = ConsoleThread(self)
        self.console.daemon = True
        
        self.logger.info("Starting up WebSocketServer...")
        self.ws.start()

        self.logger.info("Staring up Console Interface...")
        self.console.start()
        self.handle_messages()

    def shutdown(self):
        self._fromConsole.put('shutdown')

    def handle_from_console(self):
        try:
            self.logger.debug("Handling messages....")
            msg = self._fromConsole.get_nowait()
            if msg == "shutdown":
                sys.exit(0)
        except Empty:
            pass

    def handle_messages(self):
        while True:
            self.handle_from_console()


    
