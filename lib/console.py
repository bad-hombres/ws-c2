from threading import Thread
from logging import Logger
from helpers import Colour
from cmd import Cmd

class ConsoleInterface(Cmd):
    def __init__(self, server):
        Cmd.__init__(self)
        self.logger = Logger("console")
        self.server = server
        self.prompt = "[" + Colour.red("no agent", bold=True) + "]#>"

    def do_exit(self, line):
        self.logger.debug(line)
        self.server.shutdown()

class ConsoleThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
        self.logger = Logger("console")

    def run(self):
        interface = ConsoleInterface(self.server)
        interface.cmdloop()

