import gevent.queue
import gevent.socket
import os
import six

_CA_CERTS = None

try:
    from ssl import get_default_verify_paths
except ImportError:
    _CA_CERTS = None
else:
    _certs = get_default_verify_paths()
    _CA_CERTS = _certs.cafile or _certs.capath

if not _CA_CERTS or os.path.isdir(_CA_CERTS):
    import certifi
    _CA_CERTS = certifi.where()

try:
    from ssl import _DEFAULT_CIPHERS
except ImportError:
    # ssl._DEFAULT_CIPHERS in python2.7 branch.
    _DEFAULT_CIPHERS = (
        'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
        'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:ECDH+RC4:'
        'DH+RC4:RSA+RC4:!aNULL:!eNULL:!MD5')

try:
    from gevent import lock
except ImportError:
    # gevent < 1.0b2
    from gevent import coros as lock

DEFAULT_CONNECTION_TIMEOUT = 5.0
DEFAULT_NETWORK_TIMEOUT = 5.0

IGNORED = object()


class ConnectionPool(object):
    DEFAULT_CONNECTION_TIMEOUT = 5.0
    DEFAULT_NETWORK_TIMEOUT = 5.0

    def __init__(self,
                 connection_host,
                 connection_port,
                 request_host,
                 request_port,
                 size=5, disable_ipv6=False,
                 connection_timeout=DEFAULT_CONNECTION_TIMEOUT,
                 network_timeout=DEFAULT_NETWORK_TIMEOUT,
                 use_proxy=False):
        self._closed = False
        self._connection_host = connection_host
        self._connection_port = connection_port
        self._request_host = request_host
        self._request_port = request_port
        self._semaphore = lock.BoundedSemaphore(size)
        self._socket_queue = gevent.queue.LifoQueue(size)
        self._use_proxy = use_proxy

        self.connection_timeout = connection_timeout
        self.network_timeout = network_timeout
        self.size = size
        self.disable_ipv6 = disable_ipv6

    def _resolve(self):
        """ resolve (dns) socket informations needed to connect it.
        """
        family = 0
        if self.disable_ipv6:
            family = gevent.socket.AF_INET
        info = gevent.socket.getaddrinfo(self._connection_host,
                                         self._connection_port,
                                         family, 0, gevent.socket.SOL_TCP)
        # family, socktype, proto, canonname, sockaddr = info[0]
        return info

    def close(self):
        self._closed = True
        while not self._socket_queue.empty():
            try:
                sock = self._socket_queue.get(block=False)
                try:
                    sock.close()
                except:
                    pass
            except gevent.queue.Empty:
                pass

    def _create_tcp_socket(self, family, socktype, protocol):
        """ tcp socket factory.
        """
        sock = gevent.socket.socket(family, socktype, protocol)
        return sock

    def _create_socket(self):
        """ might be overridden and super for wrapping into a ssl socket
            or set tcp/socket options
        """
        sock_infos = self._resolve()
        first_error = None
        for sock_info in sock_infos:
            try:
                sock = self._create_tcp_socket(*sock_info[:3])
            except Exception as e:
                if not first_error:
                    first_error = e
                continue

            try:
                sock.settimeout(self.connection_timeout)
                sock = self._connect_socket(sock, sock_info[-1])
                self.after_connect(sock)
                sock.settimeout(self.network_timeout)
                return sock
            except IOError as e:
                sock.close()
                if not first_error:
                    first_error = e
            except:
                sock.close()
                raise

        if first_error:
            raise first_error
        else:
            raise RuntimeError(
                "Cannot resolve %s:%s" % (self._host, self._port))

    def after_connect(self, sock):
        pass

    def _connect_socket(self, sock, address):
        sock.connect(address)
        self._setup_proxy(sock)
        return sock

    def _setup_proxy(self, sock):
        if self._use_proxy:
            sock.send(
                six.binary_type(
                    "CONNECT {self._request_host}:{self._request_port} "
                    "HTTP/1.1\r\n\r\n".format(self=self),
                    'utf8'
                )
            )

            resp = sock.recv(4096)
            parts = resp.split()
            if not parts or parts[1] != b"200":
                raise RuntimeError(
                    "Error response from Proxy server : %s" % resp)

    def get_socket(self):
        """ get a socket from the pool. This blocks until one is available.
        """
        self._semaphore.acquire()
        if self._closed:
            raise RuntimeError('connection pool closed')
        try:
            return self._socket_queue.get(block=False)
        except gevent.queue.Empty:
            try:
                return self._create_socket()
            except:
                self._semaphore.release()
                raise

    def return_socket(self, sock):
        """ return a socket to the pool.
        """
        if self._closed:
            try:
                sock.close()
            except:
                pass
            return
        self._socket_queue.put(sock)
        self._semaphore.release()

    def release_socket(self, sock):
        """ call when the socket is no more usable.
        """
        try:
            sock.close()
        except:
            pass
        if not self._closed:
            self._semaphore.release()


try:
    import gevent.ssl

    try:
        from gevent.ssl import match_hostname
    except ImportError:
        from backports.ssl_match_hostname import match_hostname
except ImportError:
    pass
else:
    class SSLConnectionPool(ConnectionPool):
        """ SSLConnectionPool creates connections wrapped with SSL/TLS.

        :param host: hostname
        :param port: port
        :param ssl_options: accepts any options supported by `ssl.wrap_socket`
        :param ssl_context_factory: use `ssl.create_default_context` by default
            if provided. It must be a callable that returns a SSLContext.
        """

        default_options = {
            'ciphers': _DEFAULT_CIPHERS,
            'ca_certs': _CA_CERTS,
            'cert_reqs': gevent.ssl.CERT_REQUIRED
        }

        ssl_context_factory = getattr(gevent.ssl, "create_default_context",
                                      None)

        def __init__(self,
                     connection_host,
                     connection_port,
                     request_host,
                     request_port, **kw):
            self.ssl_options = kw.pop("ssl_options", {})
            self.ssl_context_factory = kw.pop('ssl_context_factory', None)
            self.insecure = kw.pop('insecure', False)
            super(SSLConnectionPool, self).__init__(connection_host,
                                                    connection_port,
                                                    request_host,
                                                    request_port,
                                                    **kw)

        def after_connect(self, sock):
            super(SSLConnectionPool, self).after_connect(sock)
            if not self.insecure:
                match_hostname(sock.getpeercert(), self._request_host)

        def _connect_socket(self, sock, address):
            sock = super(SSLConnectionPool, self)._connect_socket(sock, address)

            if self.ssl_context_factory is None:
                ssl_options = self.default_options.copy()
                ssl_options.update(self.ssl_options)
                return gevent.ssl.wrap_socket(sock, **ssl_options)
            else:
                return self.ssl_context_factory().wrap_socket(sock,
                                                              **self.ssl_options)
