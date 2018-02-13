from __future__ import print_function
import socket
import sys
import os
import threading

from .configuration import settings, configure
from .cli import args


__version__ = '0.1.1'


def main():
    if args.version:
        print(__version__)
        return
    configure()
    from .job import Job
    thread_pool = [threading.Thread(target=Job.worker, name='Worker%d' % i) for i in range(1, settings.threads+1)]

    # Make sure the socket does not already exist
    try:
        os.unlink(settings.socket_file)
    except OSError:
        if os.path.exists(settings.socket_file):
            print('The socket file is already exists: %s' % settings.socket_file, file=sys.stderr)

    # Create a UDS socket
    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print('Listening on %s' % settings.socket_file)
    unix_socket.bind(settings.socket_file)
    unix_socket.listen(settings.backlog)

    for thread in thread_pool:
        thread.daemon = True
        thread.start()

    while True:
        # Wait for a connection
        print('Waiting for a connection')
        connection, client_address = unix_socket.accept()
        Job.put(Job(connection, client_address))
