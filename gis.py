# -*- coding: utf-8 -*-
"""
gis.py
~~~~~~~~~~~~~~~~~

Minimal vector, raster and map serving over HTTP2

"""
import h2o
import ruido
import socket
import argparse


def index(args):
    """Add data to the index
    """
    return "[]"


def query(args):
    """Query the existing index
    """
    return "[]"


def run(args):
    """Runs openapi compatible service to serve the data
    """
    # sample h2o handler
    class Handler(h2o.Handler):
        def on_req(self):
            self.res_status = 200
            self.send_inline(b'Hello, world!')
            return 0

    config = h2o.Config()
    host = config.add_host(b'default', 65535)
    host.add_path(b'/').add_handler(Handler)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((args.host, args.port))
    sock.listen(0)

    loop = h2o.Loop()
    loop.start_accept(sock.fileno(), config)
    while loop.run() == 0:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vector, raster and maps',
                                     epilogue='Because features and pixels matter.')
    subparsers = parser.add_subparsers(help='Command to be run')

    parser_run = subparsers.add_parser('run', help='Run http service')
    parser_run.add_argument('-port', type=int, default=8443)
    parser_run.add_argument('-host', default='127.0.0.1')
    parser_run.set_defaults(func=run)

    parser_index = subparsers.add_parser('index', help='Index vector or raster data')
    parser_index.add_argument('-dir', default='.')
    parser_index.set_defaults(func=index)

    parser_query = subparsers.add_parser('run', help='Run http service')
    parser_query.add_argument('-index', default='.catalog')
    parser_query.add_argument('-query', default='find {}')
    parser_query.set_defaults(func=query)

    args = parser.parse_args()

    # Every subcommand defines a func method pointing to the implementation
    # we it is not present we should assume no command was specified and show
    # the general help.
    if not hasattr(args, 'func'):
        parser.print_help()

    # Invokes the implementation for the command with the arguments defined
    # in the subparser.
    args.func(args)
