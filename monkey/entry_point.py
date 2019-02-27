import argparse
import sys
from os import path

from cli import Launcher
from monkey import __version__

class MonkeyMainLauncher(Launcher):

    def __init__(self):
        self.parser = parser = argparse.ArgumentParser(
            description='Monkey command line interface.'
        )
        parser.add_argument(
            '-c', '--config-file',
            help='The configuration file to load settings from.'
        )
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=__version__,
            help='Show the version of the app.'
        )

        subparsers = parser.add_subparsers(
            title='Monkey sub commands',
            prog=path.basename('monkey'),
            dest='command'
        )

        from pop import Pop
        Pop.register(subparsers)

        from listen import Listen
        Listen.register(subparsers)

    def launch(self, args=None):
        cli_args = self.parser.parse_args(args if args else None)
        if hasattr(cli_args, 'func'):
            cli_args.func(cli_args)
        else:
            self.parser.print_help()
        sys.exit(0)

    @classmethod
    def create_parser(cls, subparsers):
        """
        Do nothing here
        """
        pass


def main():
    MonkeyMainLauncher()()

