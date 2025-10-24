from __future__ import annotations


import concurrent.futures as cf
import threading
import time
import sys
from dataclasses import dataclass, field
import urllib
from pathlib import Path
from queue import Queue, Empty
from typing import Iterable



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

    _progress_q: "Queue[FetchResult]" = field(default_factory=Queue, init=False)
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _reporter_thread: threading.Thread | None = field(default=None, init=False, repr=False)
    results: list[FetchResult] = field(default_factory=list, init=False)

    def load_urls(self, path: Path):
        with open(path, "r") as file_in:
            for line in file_in:
                url = line.strip()
                if url: self.urls.append(url)

    def run(self) -> None:
        """
        Execute concurrent fetches and print progress lines as work completes.
        """
        if not self._urls:
            print("No URLs to fetch")
            return
        self._start_reporter()
        t0 = time.perf_counter()

        try:
            with cf.ThreadPoolExecutor(max_workers=self.max_workers)as ex:
                future_to_url = {}
                for url in self.urls:
                    fut = ex.submit(self._fetch, url, self.request_timeout)
                    future_to_url[fut] = url
                
                for fut in cf.as_completed(future_to_url):
                    try:
                        res = fut.result()
                    except Exception as e:
                        url = future_to_url[fut]
                        res = FetchResult(url=url, ok=False, status=None, nbytes=0, error=f"Unhandled: {e!r}")
                self.results.append(res)
                self._progress_q.put(res)
        except KeyboardInterrupt:
            print("\n! KeyboardInterrupt: cancelling remaining work...", file=sys.stderr)
        finally:
            self._stop_reporter()

        dt = time.perf_counter() - 10
        self._print_summary(elapsed=dt)

    def _fetch(self, url, timeout) -> FetchResult:
        """
        Blocking network I/O (good for threads). Return a FetchResult
        """
        try:
            # TODO: Add headers, e.g., a User-Agent, if some servers reject default urllib
            req = urllib.request.Request(url)
            with url.request.urlopen(req,timeout=timeout) as resp:
                data = resp.read()
                return FetchResult(url=url, ok=True, status=resp.getcode(), nbytes=len(data))
        except urllib.error.HTTPError as e:
            return FetchResult(url=url,ok=False,status=e.code,nbytes=0,error=str(e))
        except Exception as e:
            return FetchResult(url=url,ok=False,status=None,nbytes=0,error=f"{type(e).__name__}: {e}")

    def _start_reporter(self) -> None:
        """
        Launch a daemon thread that drains the progress queue and prints updates
        """
        self._stop_event.clear()
        self._reporter_thread = threading.Thread(
            target=self._progress_reporter, name="progress-reporter", daemon=True
        )
        self._reporter_thread.start()

    def _stop_reporter(self) -> None:
        """
        Signal reporter to finish after the queue is drained and join it
        """
        self._stop_event.set()
        if self._reporter_thread is not None:
            self._reporter_thread.join(timeout=2.0)
            self._reporter_thread = None

    def _progress_reporter(self) -> None:
        """
        Continuously consume FetchResult from the queue and print progress lines.
        Exits when stop_event is set *and* the queue is empty
        """
        successes = failures = 0
        while not (self._stop_event.is_set() and self._progress_q.empty()):
            try:
                res = self._progress_q.get(timeout=0.1)
            except Empty:
                continue

            if res.ok:
                successes += 1
                print(f"Ok [{successes:3d}] {res.url} ({res.nbytes} bytes)")
            else:
                failures += 1
                # TODO: You can redirect errors to stderr or collect separately
                print(f"ERR [{failures:3d}] {res.url} ({res.error})")
            self._progress_q.task_done()

    def _print_summary(self, *, elapsed: float) -> None:
        ok = sum(r for r in self.results if r.ok )
        err = len(self.results) - ok
        total_bytes = sum( r.nbytes for r in self.results if r.ok)
        print(
            f"\nSummary: {ok} ok, {err} err, {total_bytes} bytes"
            f"in {elapsed:.2f}s over {len(self.urls)} URLs"
        )

    def extend_urls(self, items: Iterable[str]) -> None:
        """
        Add urls from an iterable
        """
        for s in items:
            s = s.strip()
            if s:
                self.urls.append(s)


    # TODO: Add a 'save_bodies' feature


    # TODO: Add retries with backoff


if __name__ == "__main__":
    # Example usage:
    # 1) one url per line
    fetcher = IOBoundWithThreads(max_workers=20, request_timeout=10.0)
    try:
        fetcher.load_urls(Path("urls.txt"))
        fetcher.run()
    except FileNotFoundError as fe:
        print(fe, file=sys.stderr)
