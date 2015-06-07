import sys
import argparse

from zeroless import Client
from .helpers import (add_sub_commands, run)

def get_parser():
    parser = argparse.ArgumentParser(prog='Zeroless Client Cli',
                                     description="""The Zeroless Client Cli shall connect to the specified
                                                 endpoint using the chosen ØMQ messaging pattern""")
    parser.add_argument('-i', '--ip', type=str,
                        default='127.0.0.1',
                        help="the IP of the endpoint to connect to (default=127.0.0.1)")

    add_sub_commands(parser)
    return parser

def zeroclient(args):
    parser = get_parser()
    parsed_args = parser.parse_args(args)
    client = Client()
    client.connect(parsed_args.ip, parsed_args.port)
    socket_executor = parsed_args.socket_executor(client, parsed_args)

    return socket_executor

def main(args=sys.argv[1:]):
    socket_executor = zeroclient(args)

    while True:
        run(socket_executor)