# -*- coding: utf-8 -*-

"""
    
    multiprocess stdout 
    
"""

from queue import Queue


class ProcessStdout(object):
    def __init__(self):
        self.__message_queue = Queue(100)

    @property
    def queue(self):
        return self.__message_queue

    def write(self, message):
        self.__message_queue.put(message)

    def read(self):
        message = self.__message_queue.get()
        return message

    def run_forever(self):
        while True:
            print(self.read())
