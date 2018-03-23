# -*- coding: utf-8 -*-
"""
gis.py
~~~~~~~~~~~~~~~~~

Minimal vector, raster and map serving over HTTP2

"""
import socket
import argparse
import sys
import glob
import os
import http


def index(args):
    """Add data to the index
    """
    import ruido
    directory = args.dir
    vectors = glob.glob(os.path.join(directory, '**', '*.json'), recursive=True)
    rasters = glob.glob(os.path.join(directory, '**', '*.tiff'), recursive=True)
    if args.verbose:
        print("Indexing %s" % directory)
        print("Vectors: %s" % vectors)
        print("Rasters: %s" % rasters)  

    for vector in vectors:
        with open(vector, 'r') as v:
            for item_raw in v:
                item = item_raw.strip(u'\u001e')
                ruido.add(os.path.join(".index", vector), item)

    return "[]"


def query(args):
    """Query the existing index
    """
    import ruido
    ruido.query('.index', 'find {} return .')
    return "[]"


def server(args):
    """Runs openapi compatible service to serve the data
    """
    handler_class = http.server.SimpleHTTPRequestHandler
    test(HandlerClass=handler_class, port=args.port, bind=args.bind)    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vector, raster and maps')
    subparsers = parser.add_subparsers(help='Command to be run')

    parser_server = subparsers.add_parser('server', help='Run http service')
    parser_server.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser_server.add_argument('port', action='store',
                        default=8443, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8443]')

    parser_server.set_defaults(func=server)

    parser_index = subparsers.add_parser('index', help='Index vector or raster data')
    parser_index.add_argument('--dir', default='.')
    parser_index.add_argument('--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    parser_index.set_defaults(func=index)

    parser_query = subparsers.add_parser('query', help='Query the gis database')
    parser_query.add_argument('-index', default='.catalog')
    parser_query.add_argument('-query', default='find {}')
    parser_query.set_defaults(func=query)

    args = parser.parse_args()

    # Every subcommand defines a func method pointing to the implementation
    # we it is not present we should assume no command was specified and show
    # the general help.
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit("No command supplied")
    # Invokes the implementation for the command with the arguments defined
    # in the subparser.
    args.func(args)
