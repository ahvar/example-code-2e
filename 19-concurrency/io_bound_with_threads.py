from __future__ import annotations


import concurrent.futures as cf
import threading
import time
import sys
from dataclasses import dataclass, field
import urllib
from pathlib import Path
from queue import Queue



@dataclass(slots=True)
class FetchResult:
    url: str
    ok: bool
    status: int | None
    nbytes: int
    error: str | None = None


@dataclass
class IOBoundWithThreads:

    max_workers: int = 20
    request_timeout: float = 10.0
    urls: list[str] = field(default_factory=list)

    _progress_q: "Queue[FetchResult]" = field(default_factory=Queue)
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _reporter_thread: threading.Thread | None = field(default=None, init=False, repr=False)
    results: list[FetchResult] = field(default_factory=list, init=False)

    def __init__(self):
        self._urls = []
        self._progress_queue = Queue()
        self._size = len(self._progress_queue)

    def read_urls(self, path: Path):
        with open(path, "r") as file_in:
            new_url = file_in.readline()
            self._urls.append(new_url)
            

    def fetch(url, timeout):
        response = urllib.request(url)

    def progress_reporter(self):
        pass


if __name__ == "__main__":
    io_bound = IOBoundWithThreads()
