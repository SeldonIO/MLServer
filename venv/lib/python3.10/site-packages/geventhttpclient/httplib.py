import six
if six.PY3:
    httplib = __import__('http.client').client
else:
    httplib = __import__('httplib')
from geventhttpclient import response
from geventhttpclient import header
import gevent.socket



class HTTPLibHeaders(header.Headers):

    def __getitem__(self, key):
        value = super(HTTPLibHeaders, self).__getitem__(key)
        if isinstance(value, (list, tuple)):
            return ", ".join(value)
        else:
            return value


class HTTPResponse(response.HTTPSocketResponse):

    def __init__(self, sock, method='GET', strict=0, debuglevel=0,
            buffering=False, **kw):
        if method is None:
            method = 'GET'
        else:
            method = method.upper()
        super(HTTPResponse, self).__init__(sock, method=method, **kw)

    @property
    def msg(self):
        if hasattr(self, '_msg'):
            return self._msg
        self._msg = HTTPLibHeaders(self._headers_index)
        return self._msg

    @property
    def fp(self):
        return self

    @property
    def version(self):
        v = self.get_http_version()
        if v == 'HTTP/1.1':
            return 11
        return 10

    @property
    def status(self):
        return self.status_code

    @property
    def reason(self):
        return self.msg

    def _read_status(self):
        return (self.version, self.status_code, self.msg)

    def begin(self):
        pass

    def close(self):
        self.release()

    def isclosed(self):
        return self._sock is None

    def read(self, amt=None):
        return super(HTTPResponse, self).read(amt)

    def getheader(self, name, default=None):
        return self.get(name.lower(), default)

    def getheaders(self):
        return self._headers_index.items()

    @property
    def will_close(self):
        return self.message_complete and not self.should_keep_alive()

    def _check_close(self):
        return not self.should_keep_alive()


HTTPLibConnection = httplib.HTTPConnection


class HTTPConnection(httplib.HTTPConnection):

    response_class = HTTPResponse

    def __init__(self, *args, **kw):
        HTTPLibConnection.__init__(self, *args, **kw)
        # python 2.6 compat
        if not hasattr(self, "source_address"):
            self.source_address = None

    def connect(self):
        self.sock = gevent.socket.create_connection(
            (self.host,self.port),
            self.timeout, self.source_address)

        if self._tunnel_host:
            self._tunnel()

try:
    import gevent.ssl
except:
    pass
else:
    class HTTPSConnection(HTTPConnection):

        default_port = 443

        def __init__(self, host, port=None, key_file=None, cert_file=None, **kw):
            HTTPConnection.__init__(self, host, port, **kw)
            self.key_file = key_file
            self.cert_file = cert_file

        def connect(self):
            "Connect to a host on a given (SSL) port."

            sock = gevent.socket.create_connection((self.host, self.port),
                                            self.timeout, self.source_address)
            if self._tunnel_host:
                self.sock = sock
                self._tunnel()
            self.sock = gevent.ssl.wrap_socket(
                sock, self.key_file, self.cert_file)


def patch():
    httplib.HTTPConnection = HTTPConnection
    httplib.HTTPResponse = HTTPResponse
    try:
        httplib.HTTPSConnection = HTTPSConnection
    except NameError:
        pass

