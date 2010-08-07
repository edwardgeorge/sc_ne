"""oscwsb.py: OSC to WebSockets bridge."""
import optparse

import eventlet
from eventlet import wsgi, websocket
import eventlet.event
from eventlet.green import select
import liblo  # requires pyliblo with my patch.
import simplejson

class Server(object):
    def __init__(self):
        self.clients = []
        self.servers = []
        self.websockets = []
        self._evt = eventlet.event.Event()
        self.wsgi_application = websocket.WebSocketWSGI(
            lambda ws: self.websocket_handler(ws))

    def handle_osc(self, path, args, types, src):
        data = simplejson.dumps([path, args])
        for s in self.websockets:
            s.send(data)

    def setup_client(self, host, port):
        address = liblo.Address(host, port)
        self.clients.append(clients)

    def setup_server(self, port):
        server = liblo.Server(port)
        self.servers.append(server)

    def run(self):
        self._evt.wait()
        while True:
            r, w, x = select.select(self.servers, [], [])
            for s in r:
                s.recv(0)

    def handle_websocket_msgt(self, msg):
        path, args = simplejson.loads(msg)
        for a in self.clients:
            liblo.send(a, path, *args)

    def websocket_handler(self, ws):
        self.connections.append(ws)
        try:
            while True:
                msg = ws.wait()
                self.handle_websocket_msg(msg)
        finally:
            self.websockets.remove(ws)


def setup(addr, client_addrs=[], server_ports=[]):
    server = Server()
    for c_host, c_port in client_addrs:
        server.setup_client(c_host, c_port)
    for s_port in server_ports:
        server.setup_server(s_port)
    eventlet.spawn(server.run)
    sock = eventlet.listen(addr)
    wsgi.server(sock, server.wsgi_application)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-c', action='append', dest='client_addrs')
    parser.add_option('-s', action='append', type='int', dest='server_ports')
    parser.add_option('-a', action='store', dest='http_address', default='')
    parser.add_option('-p', action='store', type='int', dest='http_port', default=8000)

    options, arguments = parser.parse_args()

    if not options.client_addrs and not options.server_ports:
        parser.error('this doesn\'t really do much if no servers or clients'
            ' are specified.')

    if options.client_addrs:
        c_addrs = [(a, int(p)) for i in options.client_addrs for a,p in i.split()]
    else:
        c_addrs = []

    setup((options.http_address, options.http_port), c_addrs,
          options.server_ports if options.server_ports else [])
