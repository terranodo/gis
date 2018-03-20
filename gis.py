# -*- coding: utf-8 -*-
"""
gis.py
~~~~~~~~~~~~~~~~~

An async HTTP/2 server with asyncpg support.

"""
import asyncio
import io
import json
import ssl
import collections
import argparse

from typing import List, Tuple

from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import (
    ConnectionTerminated, DataReceived, RequestReceived, StreamEnded
)
from h2.errors import ErrorCodes
from h2.exceptions import ProtocolError


RequestData = collections.namedtuple('RequestData', ['headers', 'data'])


class H2Protocol(asyncio.Protocol):
    def __init__(self):
        config = H2Configuration(client_side=False, header_encoding='utf-8')
        self.conn = H2Connection(config=config)
        self.transport = None
        self.stream_data = {}

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.conn.initiate_connection()
        self.transport.write(self.conn.data_to_send())

    def data_received(self, data: bytes):
        try:
            events = self.conn.receive_data(data)
        except ProtocolError as e:
            self.transport.write(self.conn.data_to_send())
            self.transport.close()
        else:
            self.transport.write(self.conn.data_to_send())
            for event in events:
                if isinstance(event, RequestReceived):
                    self.request_received(event.headers, event.stream_id)
                elif isinstance(event, DataReceived):
                    self.receive_data(event.data, event.stream_id)
                elif isinstance(event, StreamEnded):
                    self.stream_complete(event.stream_id)
                elif isinstance(event, ConnectionTerminated):
                    self.transport.close()

                self.transport.write(self.conn.data_to_send())

    def request_received(self, headers: List[Tuple[str, str]], stream_id: int):
        headers = collections.OrderedDict(headers)
        method = headers[':method']

        # We only support GET and POST.
        if method not in ('GET', 'POST'):
            self.return_405(headers, stream_id)
            return

        # Store off the request data.
        request_data = RequestData(headers, io.BytesIO())
        self.stream_data[stream_id] = request_data

    def stream_complete(self, stream_id: int):
        """
        When a stream is complete, we can send our response.
        """
        try:
            request_data = self.stream_data[stream_id]
        except KeyError:
            # Just return, we probably 405'd this already
            return

        headers = request_data.headers
        body = request_data.data.getvalue().decode('utf-8')

        data = json.dumps(
            {"headers": headers, "body": body}, indent=4
        ).encode("utf8")

        response_headers = (
            (':status', '200'),
            ('content-type', 'application/json'),
            ('content-length', str(len(data))),
            ('server', 'asyncio-h2'),
        )
        self.conn.send_headers(stream_id, response_headers)
        self.conn.send_data(stream_id, data, end_stream=True)

    def return_405(self, headers: List[Tuple[str, str]], stream_id: int):
        """
        We don't support the given method, so we want to return a 405 response.
        """
        response_headers = (
            (':status', '405'),
            ('content-length', '0'),
            ('server', 'asyncio-h2'),
        )
        self.conn.send_headers(stream_id, response_headers, end_stream=True)

    def receive_data(self, data: bytes, stream_id: int):
        """
        We've received some data on a stream. If that stream is one we're
        expecting data on, save it off. Otherwise, reset the stream.
        """
        try:
            stream_data = self.stream_data[stream_id]
        except KeyError:
            self.conn.reset_stream(
                stream_id, error_code=ErrorCodes.PROTOCOL_ERROR
            )
        else:
            stream_data.data.write(data)


def get_ssl_context(certfile="cert.crt", keyfile="cert.key"):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
    )
    ssl_context.set_ciphers("ECDHE+AESGCM")
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    ssl_context.set_alpn_protocols(["h2"])
    return ssl_context


def get_server(host='127.0.0.1', port=8443,
               ssl_context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)):
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(H2Protocol, host, port, ssl=ssl_context)
    server = loop.run_until_complete(coro)
    return server, loop


def run():
    ssl_context = get_ssl_context()
    server, loop = get_server(ssl_context=ssl_context)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GIS data server.')
    parser.add_argument('command', metavar='command',
                        help='Command to be run. Options are: ["run",]')

    args = parser.parse_args()
    if args.command == 'run':
        run()
