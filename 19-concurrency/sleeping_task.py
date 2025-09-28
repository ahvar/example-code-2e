"""
Sometimes, we may need to create additional threads within our Python process to execute tasks concurrently.
Python provides real naive (system level) threads
"""
from time import sleep
from threading import Thread

def task():
    sleep(1)
    print('This is coming from another thread')

thread = Thread(target=task)
thread.start()
print('Waiting for thread to finish....')
# wait for task to complete
thread.join()

