
import sys
import argparse


parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument(
    '-c', '--config-file',
    help='The configuration file to load settings from.'
)
parser.add_argument(
    '-V', '--version',
    action='store_true',
    help='Show the version of the app.'
)
args = parser.parse_args()
