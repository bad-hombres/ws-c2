from lib.application import MainApplicationThread
import Queue
import sys
import time

s = MainApplicationThread(port=8888, debug=True)
s.daemon = True
s.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
        
