# -*- coding: utf-8 -*-
import logging

def run_cherrypy_server(host="127.0.0.1", port=9000):
    """
    Runs a CherryPy server on Python 2.x.
    """
    import cherrypy

    from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
    from ws4py.websocket import EchoWebSocket

    cherrypy.config.update({'server.socket_host': host,
                            'server.socket_port': port,
                            'engine.autoreload_on': False,
                            'log.screen': False})
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    class Root(object):
        @cherrypy.expose
        def index(self):
            pass

    config = {
        '/': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': EchoWebSocket
            }
        }
    logger = logging.getLogger('autobahn_testsuite')
    logger.warning("Serving CherryPy server on %s:%s" % (host, port))

    cherrypy.quickstart(Root(), '/', config)

def run_cherrypy_server_with_wsaccel(host="127.0.0.1", port=9006):
    """
    Runs a CherryPy server on Python 2.x with
    a cython driver for some internal operations.
    """
    import wsaccel
    wsaccel.patch_ws4py()
    run_cherrypy_server(host, port)


def run_cherrypy_server_with_python3(host="127.0.0.1", port=9004):
    """
    Runs a CherryPy server on Python 3.x
    """
    run_cherrypy_server(host, port)


def run_cherrypy_server_with_pypy(host="127.0.0.1", port=9005):
    """
    Runs a CherryPy server on PyPy
    """
    run_cherrypy_server(host, port)


def run_gevent_server(host="127.0.0.1", port=9001):
    """
    Runs a gevent server on Python 2.x
    """
    from gevent import monkey; monkey.patch_all()
    from ws4py.websocket import EchoWebSocket
    from ws4py.server.geventserver import WebSocketWSGIApplication, WSGIServer

    server = WSGIServer((host, port), WebSocketWSGIApplication(handler_cls=EchoWebSocket))
    logger = logging.getLogger('autobahn_testsuite')
    logger.warning("Serving gevent server on %s:%s" % (host, port))
    server.serve_forever()


def run_python3_asyncio(host="127.0.0.1", port=9007):
    """
    Runs a server using asyncio and Python 3.3+
    """
    import asyncio
    from ws4py.async_websocket import EchoWebSocket
    from ws4py.server.tulipserver import WebSocketProtocol
    
    loop = asyncio.get_event_loop()

    def start_server():
        proto_factory = lambda: WebSocketProtocol(EchoWebSocket)
        return loop.create_server(proto_factory, host, port)

    s = loop.run_until_complete(start_server())
    logger = logging.getLogger('asyncio_testsuite')
    logger.warning("Serving asyncio server on %s:%s" % s.sockets[0].getsockname())
    loop.run_forever()



def run_tornado_server(host="127.0.0.1", port=9007):
    """
    Runs a Tornado server on Python 2.x
    """
    from tornado import ioloop, web, websocket
    class EchoWebSocket(websocket.WebSocketHandler):
        def on_message(self, message):
            self.write_message(message)

    app = web.Application([(r"/", EchoWebSocket)])
    app.listen(port, address=host)
    logger = logging.getLogger('autobahn_testsuite')
    logger.warning("Serving Tornado server on %s:%s" % (host, port))
    ioloop.IOLoop.instance().start()

def run_autobahn_server(host="127.0.0.1", port=9003):
    """
    Runs a Autobahn server on Python 2.x
    """
    from autobahntestsuite import choosereactor
    import autobahn
    from autobahn.websocket import listenWS
    from twisted.internet import reactor
    from autobahn.websocket import WebSocketServerFactory, \
         WebSocketServerProtocol

    class ServerProtocol(WebSocketServerProtocol):
        def onMessage(self, msg, binary):
            self.sendMessage(msg, binary)

    class ServerFactory(WebSocketServerFactory):
        protocol = ServerProtocol

    factory = ServerFactory("ws://%s:%d" % (host, port))
    factory.setProtocolOptions(failByDrop=False)
    logger.warning("Serving Autobahn server on %s:%s" % (host, port))
    listenWS(factory, None)
    reactor.run()

if __name__ == '__main__':
    import argparse
    from multiprocessing import Process

    logging.basicConfig(format='%(asctime)s %(message)s')
    logger = logging.getLogger('autobahn_testsuite')
    logger.setLevel(logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument('--run-all', dest='run_all', action='store_true',
                        help='Run all servers backend')
    parser.add_argument('--run-cherrypy-server', dest='run_cherrypy', action='store_true',
                        help='Run the CherryPy server backend')
    parser.add_argument('--run-cherrypy-server-wsaccel', dest='run_cherrypy_wsaccel', action='store_true',
                        help='Run the CherryPy server backend and wsaccel driver')
    parser.add_argument('--run-cherrypy-server-pypy', dest='run_cherrypy_pypy', action='store_true',
                        help='Run the CherryPy server backend with PyPy')
    parser.add_argument('--run-cherrypy-server-py3k', dest='run_cherrypy_py3k', action='store_true',
                        help='Run the CherryPy server backend with Python 3')
    parser.add_argument('--run-gevent-server', dest='run_gevent', action='store_true',
                        help='Run the gevent server backend')
    parser.add_argument('--run-tornado-server', dest='run_tornado', action='store_true',
                        help='Run the Tornado server backend')
    parser.add_argument('--run-autobahn-server', dest='run_autobahn', action='store_true',
                        help='Run the Autobahn server backend')
    parser.add_argument('--run-asyncio-server', dest='run_asyncio', action='store_true',
                        help='Run the asyncio server backend')
    args = parser.parse_args()

    if args.run_all:
        args.run_cherrypy = True
        args.run_cherrypy_wsaccel = True
        args.run_gevent = True
        args.run_tornado = True
        args.run_autobahn = True
        args.run_asyncio = True

    procs = []
    logger.warning("CherryPy server: %s" % args.run_cherrypy)
    if args.run_cherrypy:
        p0 = Process(target=run_cherrypy_server)
        p0.daemon = True
        procs.append(p0)

    logger.warning("Gevent server: %s" % args.run_gevent)
    if args.run_gevent:
        p1 = Process(target=run_gevent_server)
        p1.daemon = True
        procs.append(p1)

    logger.warning("Tornado server: %s" % args.run_tornado)
    if args.run_tornado:
        p2 = Process(target=run_tornado_server)
        p2.daemon = True
        procs.append(p2)

    logger.warning("Autobahn server: %s" % args.run_autobahn)
    if args.run_autobahn:
        p3 = Process(target=run_autobahn_server)
        p3.daemon = True
        procs.append(p3)

    logger.warning("CherryPy server on PyPy: %s" % args.run_cherrypy_pypy)
    if args.run_cherrypy_pypy:
        p4 = Process(target=run_cherrypy_server_with_pypy)
        p4.daemon = True
        procs.append(p4)

    logger.warning("CherryPy server on Python 3: %s" % args.run_cherrypy_py3k)
    if args.run_cherrypy_py3k:
        p5 = Process(target=run_cherrypy_server_with_python3)
        p5.daemon = True
        procs.append(p5)

    logger.warning("CherryPy server on Python 2/wsaccel: %s" % args.run_cherrypy_wsaccel)
    if args.run_cherrypy_wsaccel:
        p6 = Process(target=run_cherrypy_server_with_wsaccel)
        p6.daemon = True
        procs.append(p6)

    logger.warning("asyncio server on Python 3: %s" % args.run_asyncio)
    if args.run_asyncio:
        p7 = Process(target=run_python3_asyncio)
        p7.daemon = True
        procs.append(p7)

    for p in procs:
        p.start()
        logging.info("Starting process... %d" % p.pid)

    for p in procs:
        p.join()

