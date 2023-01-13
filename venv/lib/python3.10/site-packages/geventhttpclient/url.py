import six
if six.PY3:
    from urllib import parse as urlparse
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
    from collections.abc import Mapping
    basestring = (str, bytes)
else:
    import urlparse
    from urllib import quote_plus, urlencode
    from collections import Mapping

DEFAULT_PORTS = {
    'http': 80,
    'https': 443
}


def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples
    :rtype: list
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')

    if isinstance(value, Mapping):
        value = value.items()

    return list(value)


class URL(object):
    """ A mutable URL class

    You build it from a url string.
    >>> url = URL('http://getgauss.com/urls?param=asdfa')
    >>> url
    URL(http://getgauss.com/urls?param=asdfa)

    You cast it to a tuple, it returns the same tuple as `urlparse.urlsplit`.
    >>> tuple(url)
    ('http', 'getgauss.com', '/urls', 'param=asdfa', '')

    You can cast it as a string.
    >>> str(url)
    'http://getgauss.com/urls?param=asdfa'

    You can change attributes.
    >>> url.host = 'infrae.com'
    >>> url
    URL(http://infrae.com/urls?auth_token=asdfaisdfuasdf&param=asdfa)
    """

    __slots__ = ('scheme', 'host', 'port', 'path', 'query', 'fragment', 'user', 'password', 'params')
    quoting_safe = ''

    def __init__(self, url=None, params=None):
        if url is not None:
            scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        else:
            scheme, netloc, path, query, fragment = 'http', '', '/', '', ''

        self.scheme = scheme
        self.fragment = fragment

        user, password, host, port = None, None, '', None
        if netloc:
            if '@' in netloc:
                user_pw, netloc = netloc.rsplit('@', 1)
                if ':' in user_pw:
                    user, password = user_pw.rsplit(':', 1)
                else:
                    user = user_pw

            if netloc.startswith('['):
                host, port_pt = netloc.rsplit(']', 1)
                host = host.strip('[]')
                if port_pt:
                    port = int(port_pt.strip(':'))
            else:
                if ':' in netloc:
                    host, port = netloc.rsplit(':', 1)
                    port = int(port)
                else:
                    host = netloc

        if not port:
            port = DEFAULT_PORTS.get(self.scheme)

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.path = path or ''
        
        self.query = query.replace(" ", "%20") # get a little closer to the behaviour of requests.utils.requote_uri
        self.params = params

    @property
    def netloc(self):
        return self.full_netloc(auth=False)

    def full_netloc(self, auth=True):
        buf = ''
        if self.user and auth:
            buf += self.user
            if self.passwort:
                buf += ':' + self.passwort
            buf += '@'

        if ':' in self.host:
            buf += '[' + self.host + ']'
        else:
            buf += self.host
        if self.port is None:
            return buf
        elif DEFAULT_PORTS.get(self.scheme) == self.port:
            return buf
        buf += ':' + str(self.port)
        return buf

    def __copy__(self):
        clone = type(self)()
        for key in self.__slots__:
            val = getattr(self, key)
            if isinstance(val, dict):
                val = val.copy()
            setattr(clone, key, val)
        return clone

    def __repr__(self):
        return "URL(%s)" % str(self)

    def __iter__(self):
        return iter((self.scheme, self.full_netloc(), self.path,
                self.query_string, self.fragment))

    def __str__(self):
        return urlparse.urlunsplit(tuple(self))

    def __eq__(self, other):
        return str(self) == str(other)
    
    @staticmethod
    def _encode_params(data):
        """Encode parameters in a piece of data.
        Will successfully encode parameters when passed as a dict or a list of
        2-tuples.
        """

        if isinstance(data, (str, bytes)):
            return data
        elif hasattr(data, 'read'):
            return data
        elif hasattr(data, '__iter__'):
            result = []
            for k, vs in to_key_val_list(data):
                if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                    vs = [vs]
                for v in vs:
                    if v is not None:
                        result.append(
                            (k.encode('utf-8') if isinstance(k, str) else k,
                             v.encode('utf-8') if isinstance(v, str) else v))
            return urlencode(result, doseq=True)
        else:
            return data
    
    @property
    def query_string(self):
        query = []
        if self.query:
            query.append(self.query)
        if self.params:
            query.append(self._encode_params(self.params))
        return "&".join(query)

    @property
    def request_uri(self):
        query = self.query_string
        if not query:
            return self.path
        return self.path + '?' + query

    def append_to_path(self, value):
        if value.startswith('/'):
            if self.path.endswith('/'):
                self.path += value[1:]
                return self.path
        elif not self.path.endswith("/"):
            self.path += "/" + value
            return self.path

        self.path += value
        return self.path

    def redirect(self, other):
        """ Redirect to the other URL, relative to the current one """
        if not isinstance(other, type(self)):
            other = type(self)(other)
        if not other.host:
            other.scheme = self.scheme
            other.host = self.host
            other.port = self.port
        if not other.path.startswith('/'):
            if self.path.endswith('/'):
                other.path = self.path + other.path
            else:
                other.path = self.path.rsplit('/', 1)[0] + '/' + other.path
        return other

    def stripped_auth(self):
        """ Remove fragment and authentication for proxy handling """
        clone = type(self)()
        # Copy all fields except fragment, username and password
        for key in self.__slots__[:5]:
            val = getattr(self, key)
            if isinstance(val, dict):
                val = val.copy()
            setattr(clone, key, val)
        return clone
