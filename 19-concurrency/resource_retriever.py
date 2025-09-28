"""
A concurrent URL retriever
"""
from typing import List
from queue import Queue
from urllib import request
from threading import Tread, Event
from concurrent.futures import ThreadPoolExecutor
class URLRetriever:
    def __init__(self, urls: List):
        self._urls = urls
        self._progress_queue = Queue()
        self._executor = ThreadPoolExecutor()


    def fetch(url: str, timeout: int):
        req = request.urlopen(url, timeout)

    def progress_reporter(self, done: Event):
        for msg in self._progress_queue:
            print(msg)



    
