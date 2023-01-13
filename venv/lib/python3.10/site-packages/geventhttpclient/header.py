import six

if six.PY3:
    from collections.abc import Mapping, MutableMapping
else:
    from collections import Mapping, MutableMapping

_dict_setitem = dict.__setitem__
_dict_getitem = dict.__getitem__
_dict_delitem = dict.__delitem__
_dict_contains = dict.__contains__
_dict_setdefault = dict.setdefault


class Headers(dict):
    """
    :param headers:
        An iterable of field-value pairs. Must not contain multiple field names
        when compared case-insensitively.

    :param kwargs:
        Additional field-value pairs to pass in to ``dict.update``.

    A ``dict`` like container for storing HTTP Headers.

    Field names are stored and compared case-insensitively in compliance with
    RFC 7230. Iteration provides the first case-sensitive key seen for each
    case-insensitive pair.

    Using ``__setitem__`` syntax overwrites fields that compare equal
    case-insensitively in order to maintain ``dict``'s api. For fields that
    compare equal, instead create a new ``Headers`` and use ``.add``
    in a loop.

    If multiple fields that are equal case-insensitively are passed to the
    constructor or ``.update``, the behavior is undefined and some will be
    lost.

    Note: b'asdf' and 'u'asdf' are separate things. This class tries not to
    enforce the one or the other.

    >>> headers = Headers()
    >>> headers.add('Set-Cookie', 'foo=bar')
    >>> headers.add('set-cookie', 'baz=quxx')
    >>> headers['content-length'] = '7'
    >>> headers['SET-cookie']
    'foo=bar, baz=quxx'
    >>> headers['Content-Length']
    '7'
    """

    def __init__(self, headers=None, **kwargs):
        dict.__init__(self)
        if headers is not None:
            if isinstance(headers, Headers):
                self._copy_from(headers)
            else:
                self.extend(headers)
        if kwargs:
            self.extend(kwargs)

    def __setitem__(self, key, val):
        return _dict_setitem(self, key.lower(), (key, val))

    def __getitem__(self, key):
        val = _dict_getitem(self, key.lower())
        if len(val) == 2:
            return val[1]
        return val[1:]

    def __delitem__(self, key):
        return _dict_delitem(self, key.lower())

    def __contains__(self, key):
        return _dict_contains(self, key.lower())

    def __eq__(self, other):
        if not isinstance(other, Mapping) and not hasattr(other, 'keys'):
            return False
        if not isinstance(other, type(self)):
            other = type(self)(other)
        return dict((k1, self[k1]) for k1 in self) == dict((k2, other[k2]) for k2 in other)

    def __ne__(self, other):
        return not self.__eq__(other)

    values = MutableMapping.values
    get = MutableMapping.get
    update = MutableMapping.update
    if six.PY3:
        keys = MutableMapping.keys
    else:
        iterkeys = MutableMapping.iterkeys
    if six.PY2:
        itervalues = MutableMapping.itervalues

    __marker = object()

    def pop(self, key, default=__marker):
        '''D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
          If key is not found, d is returned if given, otherwise KeyError is raised.
        '''
        # Using the MutableMapping function directly fails due to the private marker.
        # Using ordinary dict.pop would expose the internal structures.
        # So let's reinvent the wheel.
        try:
            value = self[key]
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def discard(self, key):
        try:
            del self[key]
        except KeyError:
            pass

    def add(self, key, val):
        """Adds a (name, value) pair, doesn't overwrite the value if it already
        exists.

        >>> headers = Headers(foo='bar')
        >>> headers.add('Foo', 'baz')
        >>> headers['foo']
        'bar, baz'
        """
        key_lower = key.lower()
        new_vals = key, val
        # Keep the common case aka no item present as fast as possible
        vals = _dict_setdefault(self, key_lower, new_vals)
        if new_vals is not vals:
            # new_vals was not inserted, as there was a previous one
            if isinstance(vals, list):
                # If already several items got inserted, we have a list
                vals.append(val)
            else:
                # vals should be a tuple then, i.e. only one item so far
                # Need to convert the tuple to list for further extension
                _dict_setitem(self, key_lower, [vals[0], vals[1], val])

    def extend(self, *args, **kwargs):
        """Generic import function for any type of header-like object.
        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
        if len(args) > 1:
            raise TypeError("extend() takes at most 1 positional "
                            "arguments ({} given)".format(len(args)))
        other = args[0] if len(args) >= 1 else ()

        if isinstance(other, Headers):
            for key, val in other.iteritems():
                self.add(key, val)
        elif isinstance(other, Mapping):
            for key in other:
                self.add(key, other[key])
        elif hasattr(other, "keys"):
            for key in other.keys():
                self.add(key, other[key])
        else:
            for key, value in other:
                self.add(key, value)

        for key, value in kwargs.items():
            self.add(key, value)

    def getlist(self, key):
        """Returns a list of all the values for the named field. Returns an
        empty list if the key doesn't exist."""
        try:
            vals = _dict_getitem(self, key.lower())
        except KeyError:
            return []
        else:
            if isinstance(vals, tuple):
                return [vals[1]]
            else:
                return vals[1:]

    # Backwards compatibility for httplib
    getheaders = getlist
    getallmatchingheaders = getlist
    iget = getlist

    # Python3 compatibility
    def get_all(self, key, failobj=None):
        vals = self.getlist(key)
        if not vals:
            return failobj
        return vals


    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, dict(self.itermerged()))

    def _copy_from(self, other):
        for key in other:
            val = _dict_getitem(other, key)
            if isinstance(val, list):
                # Don't need to convert tuples
                val = list(val)
            _dict_setitem(self, key, val)

    def copy(self):
        clone = type(self)()
        clone._copy_from(self)
        return clone

    def itermerged(self):
        """Iterate over all headers, merging duplicate ones together."""
        for key in self:
            val = _dict_getitem(self, key)
            # this should preserve either binary or string type
            sep = u', ' if isinstance(val[1], six.string_types) else b', '
            yield val[0], sep.join(val[1:])

    # Extensions to urllib3, compatibility to previous implementation
    def __len__(self):
        return sum(len(self.getlist(key)) for key in self)

    def compatible_dict(self):
        return dict(self.itermerged())

    def iterlower(self):
        for key in self:
            vals = _dict_getitem(self, key)
            for val in vals[1:]:
                yield key, val

    iteritems = iterlower

    def items(self):
        return list(self.iterlower())

    def iteroriginal(self):
        """Iterate over all header lines, including duplicate ones."""
        for key in self:
            vals = _dict_getitem(self, key)
            for val in vals[1:]:
                yield vals[0], val
