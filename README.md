WebSocket for Python (ws4py)
============================

library providing support for draft-10 of the WebSocket protocol defined in http://tools.ietf.org/html/draft-ietf-hybi-thewebsocketprotocol-10.


Getting Started
===============

Requirements
------------

As a standalone client, ws4py only requires Python 2.6.6 or above though it hasn't been ported to Python 3.x yet.

If you want to run the Tornado client and/or server, you will need Tornado 2.0.x (https://github.com/facebook/tornado)

If you want to run the CherryPy server, you will need CherryPy 3.2.1 (http://download.cherrypy.org/cherrypy/3.2.1/)


Installing
----------

In order to install ws4py you can either grab the source code and run:

 $ python setup.py install

Or use a package manager like pip and run:

 $ pip install git+git://github.com/Lawouach/WebSocket-for-Python.git

Test suite
----------

The code currently provides a few unit tests of the stream and frame processing. 
For functional testing, you can use the Autobahn project (http://www.tavendo.de/autobahn) which provides an extensive test suite.

You may try to run it against the CherryPy server as follow:

 $ python ws4py/server/cherrypyserver.py

Then from a different terminal:

 $ cd Autobahn/testsuite/websockets
 $ python fuzzing_client.py

This will run the complete suite. As of this writing, the CherryPy server passes all the functional tests but
fails on some performance tests by being too slow.

Some reports can be found for the CherryPy server http://www.defuze.org/oss/ws4py/testreports/servers/cherrypy/

Credits
-------

Many thanks to the pywebsocket and Tornado projects which have provided a good base to write ws4py.