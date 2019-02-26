
import pymlconf


settings = pymlconf.DeferredConfigManager()


BUILTIN_CONFIGURATION = """
queuemanager: TEST.QM
queue: TEST.QUEUE
channel: TEST.CHANNEL
user: mqm
password: mqm

threads: 4
socket_file: /tmp/a.s
backlog: 10
queue_size: 512
chunk: 1024
"""


def configure(filename=None):
    settings.load(builtin=BUILTIN_CONFIGURATION)
    if filename:
        settings.load_files(filename)
