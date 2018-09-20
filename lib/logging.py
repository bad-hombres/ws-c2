from helpers import Colour
import sys


class Logger(object):
    def __init__(self, target):
        self.target = target

    def __getMessage__(self, message):
        return "[{}] -> {}".format(self.target, message)

    def info(self, message):
        print Colour.blue("[+] {}".format(self.__getMessage__(message)))

    def warn(self, message):
        print Colour.yellow("[!] {}".format(self.__getMessage__(message)))
    
    def error(self, message):
        print Colour.red("[*] {}".format(self.__getMessage__(message)))

    def debug(self, message):
        print Colour.cyan("[?] {}".format(self.__getMessage__(message)))
