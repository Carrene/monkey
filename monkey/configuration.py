
import pymlconf

from cli import args


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
chunk: 2048
"""


def configure():
    settings.load(builtin=BUILTIN_CONFIGURATION)
    if args.config_file:
        settings.load_files([args.config_file])
