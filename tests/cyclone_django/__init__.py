# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
import sys
import six
import unittest
from ..utils import django
from nose import twistedtools
from twisted.python import log


def setup():
    if six.PY3:
        # Neither flask nor werkzeug support python 3.x.
        raise unittest.SkipTest('No support for python 3.x')

    # Initialize the database access layer.
    django.initialize('django')

    # Start the reactor and run the development server
    # Twistedtools spins off the reactor loop into a separate thread
    # so the tests may continue on this thread.
    from .app import application
    log.startLogging(sys.stdout)
    twistedtools.reactor.listenTCP(5000, application, interface='localhost')
    twistedtools.threaded_reactor()


def teardown():
    # Shutdown the reactor thread.
    twistedtools.stop_reactor()
