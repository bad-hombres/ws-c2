from lib.application import MainApplicationThread
import Queue
import sys
import time
from lib.helpers import banner

banner()
s = MainApplicationThread(8888)
s.run()
