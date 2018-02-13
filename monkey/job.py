from __future__ import print_function
import threading
import Queue

import pymqi

from configuration import settings


jobs = Queue.Queue(maxsize=settings.queue_size)
thread_local = threading.local()


class Job:
    def __init__(self, connection, client_address):
        self.connection = connection
        self.client_address = client_address

    @property
    def worker_name(self):
        return threading.current_thread().name

    def read_data(self):
        data = b''
        while True:
            chunk = self.connection.recv(settings.chunk)
            if not chunk:
                print(self.worker_name, 'Done')
                break
            data += chunk
            print(self.worker_name, data)
        return data

    def do(self):
        print('Doing %s' % self.worker_name)
        data = self.read_data()
        if data:
            thread_local.queue.put(data)

    @classmethod
    def worker(cls):
        thread_local.queuemanager = qm = pymqi.connect(
            settings.queuemanager,
            channel=settings.channel,
            user=settings.user,
            password=settings.password
        )
        thread_local.queue = pymqi.Queue(qm, settings.queue)

        while True:
            job = jobs.get()
            job.do()

    @classmethod
    def put(cls, item):
        jobs.put(item)
