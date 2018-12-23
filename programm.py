"""This is chronovk application"""
import sys
from argparse import ArgumentParser

from chronovk.chronovk import Vk


class Chrono():
    """Class that represents executable application"""

    def __init__(self):
        self.vk = Vk()
        parser = ArgumentParser(description='Main parser',
                                usage='''chrono <command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            raise SystemExit
        # execute command
        getattr(self, args.command)()

    def send(self):
        parser = ArgumentParser(
            description='Send message to user or group')
        parser.add_argument('id')
        parser.add_argument('message')
        args = parser.parse_args(sys.argv[2:])
        print(args.id)
        self.vk.send_message(peer_id=int(args.id), message=args.message)

    def getc(self):
        # count
        self.vk.get_conversations(count=1)

    def getm(self):
        # id count
        self.vk.get_messages()


if __name__ == "__main__":
    Chrono()
