# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
from armet import http
# from six.moves import cStringIO as StringIO
import io
import bottle
from importlib import import_module


class Request(http.Request):

    class Headers(http.request.Headers):

        def __getitem__(self, name):
            return bottle.request.headers[name]

        def __iter__(self):
            return iter(bottle.request.headers)

        def __len__(self):
            return len(bottle.request.headers)

        def __contains__(self, name):
            return name in bottle.request.headers

    def __init__(self, *args, **kwargs):
        request = bottle.request
        async = kwargs['asynchronous']
        self._handle = request.copy() if async else request
        kwargs.update(method=bottle.request.method)
        super(Request, self).__init__(*args, **kwargs)

    @property
    def protocol(self):
        return self._handle.urlparts.scheme.upper()

    @property
    def query(self):
        return self._handle.query_string

    @property
    def uri(self):
        return self._handle.url

    def _read(self, count=-1):
        return self._handle.body.read(count)

    def _readline(self, limit=-1):
        return self._handle.body.readline(limit)

    def _readlines(self, hint=-1):
        return self._handle.body.readlines(hint)


class Response(http.Response):

    class Headers(http.response.Headers):

        def __setitem__(self, name, value):
            self._obj._assert_open()
            self._obj._handle.headers[self._normalize(name)] = value

        def __getitem__(self, name):
            return self._obj._handle.headers[name]

        def __contains__(self, name):
            return name in self._obj._handle.headers

        def __delitem__(self, name):
            self._obj._assert_open()
            del self._obj._handle.headers[name]

        def __len__(self):
            return len(self._obj._handle.headers)

        def __iter__(self):
            return iter(self._obj._handle.headers)

    def __init__(self, *args, **kwargs):
        self._stream = io.BytesIO()
        self._handle = bottle.response
        super(Response, self).__init__(*args, **kwargs)
        if self.asynchronous:
            # If we're dealing with an asynchronous response, we need
            # to have a thread-safe response handle as well as an
            # asynchronous queue to give to WSGI.
            self._handle = self._handle.copy()
            self._queue = import_module('gevent.queue').Queue()

    @property
    def status(self):
        return self._handle.status_code

    @status.setter
    def status(self, value):
        self._assert_open()
        self._handle.status = value

    def clear(self):
        super(Response, self).clear()
        self._stream.truncate(0)
        self._stream.seek(0)

    def tell(self):
        return self._stream.tell() + len(self._handle.body)

    def _write(self, chunk):
        self._stream.write(chunk)

    def _push(self):
        # Point the response handle to our constructed response.
        bottle.response.status = self.status
        bottle.response.headers.update(self.headers)

    def _flush(self):
        if not self.asynchronous:
            # Nothing more to do as the write buffer is the output buffer.
            return

        # Write the buffer to the queue.
        self._queue.put(self._stream.getvalue())
        self._stream.truncate(0)
        self._stream.seek(0)

    def close(self):
        super(Response, self).close()
        if self.asynchronous:
            # Close the queue and terminate the connection.
            self._queue.put(StopIteration)
