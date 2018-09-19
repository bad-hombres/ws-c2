from lib.server import Server
import Queue
import sys
import time

s = Server(8888, Queue.Queue(0), debug=True)
s.daemon = True
s.start()

while True:
    try:
        time.sleep(1)
        
    except KeyboardInterrupt:
        sys.exit(0)
        
