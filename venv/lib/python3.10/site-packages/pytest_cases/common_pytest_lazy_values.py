# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from functools import partial
import weakref

try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature  # noqa

try:
    from typing import Union, Callable, List, Set, Tuple, Any, Sequence, Optional, Iterable  # noqa
except ImportError:
    pass

try:
    from _pytest.mark.structures import MarkDecorator, Mark  # noqa
except ImportError:
    pass

from .common_pytest_marks import get_pytest_marks_on_function, markdecorators_as_tuple, PYTEST53_OR_GREATER, \
    markdecorators_to_markinfos


class Lazy(object):
    """
    All lazy items should inherit from this for good pytest compliance (ids, marks, etc.)
    """
    __slots__ = ()

    _field_names = ()
    """Subclasses should fill this variable to get an automatic __eq__ and __repr__."""

    # @abstractmethod
    def get_id(self):
        """Return the id to use by pytest"""
        raise NotImplementedError()

    # @abstractmethod
    def get(self, request_or_item):
        """Return the actual value to use by pytest in the given context"""
        raise NotImplementedError()

    def __str__(self):
        """in pytest<5.3 we inherit from int so that str(v) is called by pytest _idmaker to get the id

        In later pytest this is extremely convenient to have this string representation
        for example to use in pytest-harvest results tables, so we still keep it.
        """
        return self.get_id()

    def __eq__(self, other):
        """Default equality method based on the _field_names"""
        try:
            return all(getattr(self, k) == getattr(other, k) for k in self._field_names)
        except Exception:  # noqa
            return False

    def __repr__(self):
        """Default repr method based on the _field_names"""

        return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, getattr(self, k))
                                                              for k in self._field_names))

    @property
    def __name__(self):
        """for pytest >= 5.3 we override this so that pytest uses it for id"""
        return self.get_id()

    @classmethod
    def copy_from(cls, obj):
        """Subclasses should override this"""
        raise NotImplementedError()

    def clone(self):
        """Clones self based on copy_from"""
        return type(self).copy_from(self)


def _unwrap(obj):
    """A light copy of _pytest.compat.get_real_func. In our case
    we do not wish to unwrap the partial nor handle pytest fixture
    Note: maybe from inspect import unwrap could do the same?
    """
    start_obj = obj
    for _ in range(100):
        # __pytest_wrapped__ is set by @pytest.fixture when wrapping the fixture function
        # to trigger a warning if it gets called directly instead of by pytest: we don't
        # want to unwrap further than this otherwise we lose useful wrappings like @mock.patch (#3774)
        # new_obj = getattr(obj, "__pytest_wrapped__", None)
        # if isinstance(new_obj, _PytestWrapper):
        #     obj = new_obj.obj
        #     break
        new_obj = getattr(obj, "__wrapped__", None)
        if new_obj is None:
            break
        obj = new_obj
    else:
        raise ValueError("could not find real function of {start}\nstopped at {current}".format(
                start=repr(start_obj), current=repr(obj)
            )
        )
    return obj


def partial_to_str(partialfun):
    """Return a string representation of a partial function, to use in lazy_value ids"""
    strwds = ", ".join("%s=%s" % (k, v) for k, v in partialfun.keywords.items())
    if len(partialfun.args) > 0:
        strargs = ', '.join(str(i) for i in partialfun.args)
        if len(partialfun.keywords) > 0:
            strargs = "%s, %s" % (strargs, strwds)
    else:
        strargs = strwds
    return "%s(%s)" % (partialfun.func.__name__, strargs)


# noinspection PyPep8Naming
class _LazyValue(Lazy):
    """
    A reference to a value getter, to be used in `parametrize`.

    A `lazy_value` is the same thing than a function-scoped fixture, except that the value getter function is not a
    fixture and therefore can neither be parametrized nor depend on fixtures. It should have no mandatory argument.

    The `self.get(request)` method can be used to get the value for the current pytest context. This value will
    be cached so that plugins can call it several time without triggering new calls to the underlying function.
    So the underlying function will be called exactly once per test node.

    See https://github.com/smarie/python-pytest-cases/issues/149
    and https://github.com/smarie/python-pytest-cases/issues/143
    """
    if PYTEST53_OR_GREATER:
        __slots__ = 'valuegetter', '_id', '_marks', 'cached_value_context', 'cached_value'
        _field_names = __slots__
    else:
        # we can not define __slots__ since we'll extend int in a subclass
        # see https://docs.python.org/3/reference/datamodel.html?highlight=__slots__#notes-on-using-slots
        _field_names = 'valuegetter', '_id', '_marks', 'cached_value_context', 'cached_value'

    @classmethod
    def copy_from(cls,
                  obj  # type: _LazyValue
                  ):
        """Creates a copy of this _LazyValue"""
        new_obj = cls(valuegetter=obj.valuegetter, id=obj._id, marks=obj._marks)
        # make sure the copy will not need to retrieve the result if already done
        new_obj.cached_value_context = obj.cached_value_context
        new_obj.cached_value = obj.cached_value
        return new_obj

    # noinspection PyMissingConstructor
    def __init__(self,
                 valuegetter,  # type: Callable[[], Any]
                 id=None,      # type: str  # noqa
                 marks=None,   # type: Union[MarkDecorator, Iterable[MarkDecorator]]
                 ):
        self.valuegetter = valuegetter
        self._id = id
        self._marks = markdecorators_as_tuple(marks)
        self.cached_value_context = None
        self.cached_value = None

    def __hash__(self):
        """Provide a minimal hash representing the class, valuegetter, id and marks"""
        return hash((self.__class__, self.valuegetter, self._id, self._marks))

    def get_marks(self,
                  as_decorators=False  # type: bool
                  ):
        # type: (...) -> Union[Tuple[Mark, ...], Tuple[MarkDecorator, ...]]
        """
        Overrides default implementation to return the marks that are on the case function

        :param as_decorators: when True, the marks (MarkInfo) will be transformed into MarkDecorators before being
            returned
        :return:
        """
        valuegetter_marks = tuple(get_pytest_marks_on_function(self.valuegetter, as_decorators=as_decorators))

        if self._marks:
            if as_decorators:
                # self_marks = markinfos_to_markdecorators(self._marks, function_marks=True)
                self_marks = self._marks
            else:
                self_marks = markdecorators_to_markinfos(self._marks)

            return self_marks + valuegetter_marks
        else:
            return valuegetter_marks

    def get_id(self):
        """The id to use in pytest"""
        if self._id is not None:
            return self._id
        else:
            # default is the __name__ of the value getter
            _id = getattr(self.valuegetter, '__name__', None)
            if _id is not None:
                return _id

            # unwrap and handle partial functions
            vg = _unwrap(self.valuegetter)

            if isinstance(vg, partial):
                return partial_to_str(vg)
            else:
                return vg.__name__

    def get(self, request_or_item):
        """
        Calls the underlying value getter function `self.valuegetter` and returns the result.

        This result is cached to ensure that the underlying getter function is called exactly once for each
        pytest node. Note that we do not cache across calls to preserve the pytest spirit of "no leakage
        across test nodes" especially when the value is mutable.

        See https://github.com/smarie/python-pytest-cases/issues/149
        and https://github.com/smarie/python-pytest-cases/issues/143

        :param request_or_item: the context of this call: either a pytest request or test node item.
        """
        node = get_test_node(request_or_item)

        if not self.has_cached_value(node=node):
            # retrieve the value by calling the function
            self.cached_value = self.valuegetter()
            # remember the pytest context of the call with a weak reference to avoir gc issues
            self.cached_value_context = weakref.ref(node)

        return self.cached_value

    def has_cached_value(self, request_or_item=None, node=None, raise_if_no_context=True):
        """Return True if there is a cached value in self.value correnponding to the given request

        A degraded query "is there a cached value" (whatever the context) can be performed by not passing any
        request, item or node, and switching `raise_if_no_context` to False.

        :param request_or_item: the pytest request or item
        :param node: the pytest node if it already known.
        :param raise_if_no_context: a boolean indicating if an error should be raised if `request_or_item` and `node`
            are both None. Default is `True`.
        """
        if node is None:
            # can we get that context information from the request/item ?
            if request_or_item is None:
                if raise_if_no_context:
                    raise ValueError("No request, item or node was provided: I can not tell if there is a "
                                     "cached value for your context. Switch `raise_if_no_context=False` if"
                                     " you wish to get a degraded answer.")
                else:
                    # degraded answer: just tell if the cache was populated at least once
                    return self.cached_value_context is not None

            # get node context information
            node = get_test_node(request_or_item)

        elif request_or_item is not None:
            raise ValueError("Only one of `request_or_item` and `node` should be provided")

        # True if there is a cached value context that is the same as the context of the request
        return self.cached_value_context is not None and self.cached_value_context() is node

    def as_lazy_tuple(self, nb_params):
        return LazyTuple(self, nb_params)

    def as_lazy_items_list(self, nb_params):
        return [v for v in self.as_lazy_tuple(nb_params)]


class _LazyTupleItem(Lazy):
    """
    An item in a Lazy Tuple
    """
    if PYTEST53_OR_GREATER:
        __slots__ = 'host', 'item'
        _field_names = __slots__
    else:
        # we can not define __slots__ since we'll extend int in a subclass
        # see https://docs.python.org/3/reference/datamodel.html?highlight=__slots__#notes-on-using-slots
        _field_names = 'host', 'item'

    @classmethod
    def copy_from(cls,
                  obj  # type: _LazyTupleItem
                  ):
        """Creates a copy of this _LazyTupleItem"""
        return cls(host=obj.host, item=obj.item)

    # noinspection PyMissingConstructor
    def __init__(self,
                 host,  # type: LazyTuple
                 item   # type: int
                 ):
        self.host = host
        self.item = item

    def __hash__(self):
        """Provide a minimal hash representing the class, host and item number"""
        return hash((self.__class__, self.host, self.item))

    def __repr__(self):
        """Override the inherited method to avoid infinite recursion"""

        # lazy value tuple or cached tuple
        if self.host.has_cached_value(raise_if_no_context=False):
            tuple_to_represent = self.host.cached_value
        else:
            tuple_to_represent = self.host._lazyvalue  # noqa

        vals_to_display = (
            ('item', self.item),  # item number first for easier debug
            ('tuple', tuple_to_represent),
        )
        return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, v) for k, v in vals_to_display))

    def get_id(self):
        return "%s[%s]" % (self.host.get_id(), self.item)

    def get(self, request_or_item):
        """ Call the underlying value getter if needed (cache), then return the result tuple item value (not self).

        See _LazyValue.get for details

        :param request_or_item: the context of this call: either a pytest request or test node item.
        """
        return self.host.force_getitem(self.item, request_or_item)


class LazyTuple(Lazy):
    """
    A wrapper representing a lazy_value used as a tuple = for several argvalues at once.

    Its `.get()` method caches the tuple obtained from the value getter, so that it is not called several times (once
    for each LazyTupleItem)

    It is only used directly by pytest when a lazy_value is used in a @ parametrize to decorate a fixture.
    Indeed in that case pytest does not unpack the tuple, we do it in our custom @fixture.

    In all other cases (when @parametrize is used on a test function), pytest unpacks the tuple so it directly
    manipulates the underlying LazyTupleItem instances.
    """
    __slots__ = '_lazyvalue', 'theoretical_size'
    _field_names = __slots__

    @classmethod
    def copy_from(cls,
                  obj  # type: LazyTuple
                  ):
        # clone the inner lazy value
        value_copy = obj._lazyvalue.clone()
        return cls(valueref=value_copy, theoretical_size=obj.theoretical_size)

    # noinspection PyMissingConstructor
    def __init__(self,
                 valueref,         # type: _LazyValue
                 theoretical_size  # type: int
                 ):
        self._lazyvalue = valueref
        self.theoretical_size = theoretical_size

    def __hash__(self):
        """Provide a minimal hash representing the class, lazy value, and theoretical size"""
        return hash((self.__class__, self._lazyvalue, self.theoretical_size))

    def __len__(self):
        return self.theoretical_size

    def get_id(self):
        """return the id to use by pytest"""
        return self._lazyvalue.get_id()

    def get(self, request_or_item):
        """ Call the underlying value getter if needed (cache), then return the result tuple value (not self).
        See _LazyValue.get for details

        :param request_or_item: the context of this call: either a pytest request or test node item.
        """
        return self._lazyvalue.get(request_or_item)

    def has_cached_value(self, request_or_item=None, node=None, raise_if_no_context=True):
        """Return True if there is a cached value correnponding to the given request

        A degraded query "is there a cached value" (whatever the context) can be performed by not passing any
        request, item or node, and switching `raise_if_no_context` to False.

        :param request_or_item: the pytest request or item
        :param node: the pytest node if it already known.
        :param raise_if_no_context: a boolean indicating if an error should be raised if `request_or_item` and `node`
            are both None. Default is `True`.
        """
        return self._lazyvalue.has_cached_value(request_or_item=request_or_item, node=node,
                                                raise_if_no_context=raise_if_no_context)

    @property
    def cached_value(self):
        return self._lazyvalue.cached_value

    def __getitem__(self, item):
        """
        Getting an item in the tuple with self[i] does *not* retrieve the value automatically, but returns
        a facade (a LazyTupleItem), so that pytest can store this item independently wherever needed, without
        yet calling the value getter.
        """
        if item >= self.theoretical_size:
            raise IndexError(item)
        else:
            # note: do not use the cache here since we do not know the context.
            # return a facade than will be able to use the cache of the tuple
            return LazyTupleItem(self, item)

    def force_getitem(self, item, request):
        """ Call the underlying value getter, then return self[i]. """
        # Note: this will use the cache correctly if needed
        argvalue = self.get(request)
        try:
            return argvalue[item]
        except TypeError as e:
            raise ValueError("(lazy_value) The parameter value returned by `%r` is not compliant with the number"
                             " of argnames in parametrization (%s). A %s-tuple-like was expected. "
                             "Returned lazy argvalue is %r and argvalue[%s] raised %s: %s"
                             % (self._lazyvalue, self.theoretical_size, self.theoretical_size,
                                argvalue, item, e.__class__, e))


if PYTEST53_OR_GREATER:
    # in the latest versions of pytest, the default _idmaker returns the value of __name__ if it is available,
    # even if an object is not a class nor a function. So we do not need to use any special trick with our
    # lazy objects
    class LazyValue(_LazyValue):
        pass

    class LazyTupleItem(_LazyTupleItem):
        pass
else:
    # in this older version of pytest, the default _idmaker does *not* return the value of __name__ for
    # objects that are not functions not classes. However it *does* return str(obj) for objects that are
    # instances of bool, int or float. So that's why we make our lazy objects inherit from int.
    fake_base = int

    class _LazyValueBase(fake_base, object):

        __slots__ = ()

        def __new__(cls, *args, **kwargs):
            """ Inheriting from int is a bit hard in python: we have to override __new__ """
            obj = fake_base.__new__(cls, 111111)  # noqa
            cls.__init__(obj, *args, **kwargs)  # noqa
            return obj

        def __getattribute__(self, item):
            """Map all default attribute and method access to the ones in object, not in int"""
            return object.__getattribute__(self, item)

        def __repr__(self):
            """Magic methods are not intercepted by __getattribute__ and need to be overridden manually.
            We do not need all of them by at least override this one for easier debugging"""
            return object.__repr__(self)

    class LazyValue(_LazyValue, _LazyValueBase):
        """Same than _LazyValue but inherits from int so that pytest calls str(o) for the id.
        Note that we do it afterwards so that _LazyValue remains "pure" - pytest-harvest needs to reuse it"""

        def clone(self, remove_int_base=False):
            if not remove_int_base:
                # return a type(self) (LazyValue or subclass)
                return _LazyValue.clone(self)
            else:
                # return a _LazyValue without the int base from _LazyValueBase
                return _LazyValue.copy_from(self)

    class LazyTupleItem(_LazyTupleItem, _LazyValueBase):
        """Same than _LazyTupleItem but inherits from int so that pytest calls str(o) for the id"""

        def clone(self, remove_int_base=False):
            if not remove_int_base:
                # return a type(self) (LazyTupleItem or subclass)
                return _LazyTupleItem.clone(self)
            else:
                # return a _LazyTupleItem without the int base from _LazyValueBase
                return _LazyTupleItem.copy_from(self)


def lazy_value(valuegetter,  # type: Callable[[], Any]
               id=None,      # type: str  # noqa
               marks=()      # type: Union[MarkDecorator, Iterable[MarkDecorator]]
               ):
    """
    Creates a reference to a value getter, to be used in `parametrize`.

    A `lazy_value` is the same thing than a function-scoped fixture, except that the value getter function is not a
    fixture and therefore can neither be parametrized nor depend on fixtures. It should have no mandatory argument.
    The underlying function will be called exactly once per test node.

    By default the associated id is the name of the `valuegetter` callable, but a specific `id` can be provided
    otherwise. Note that this `id` does not take precedence over custom `ids` or `idgen` passed to @parametrize.

    Note that a `lazy_value` can be included in a `pytest.param` without problem. In that case the id defined by
    `pytest.param` will take precedence over the one defined in `lazy_value` if any. The marks, however,
    will all be kept wherever they are defined.

    :param valuegetter: a callable without mandatory arguments
    :param id: an optional id. Otherwise `valuegetter.__name__` will be used by default
    :param marks: optional marks. `valuegetter` marks will also be preserved.
    """
    return LazyValue(valuegetter, id=id, marks=marks)


def is_lazy_value(argval):
    """ Return True if `argval` is the *immediate* output of `lazy_value()` """
    try:
        # note: we use the private and not public class here on purpose
        return isinstance(argval, _LazyValue)
    except Exception:  # noqa
        return False


def is_lazy(argval):
    """
    Return True if `argval` is the outcome of processing a `lazy_value` through `@parametrize`
    As opposed to `is_lazy_value`, this encompasses lazy tuples that are created when parametrizing several argnames
    with the same `lazy_value()`.
    """
    try:
        # note: we use the private and not public classes here on purpose
        return isinstance(argval, (_LazyValue, LazyTuple, _LazyTupleItem))
    except Exception:  # noqa
        return False


def get_lazy_args(argval, request_or_item):
    """
    Possibly calls the lazy values contained in argval if needed, before returning it.
    Since the lazy values cache their result to ensure that their underlying function is called only once
    per test node, the `request` argument here is mandatory.

    :param request_or_item: the context of this call: either a pytest request or item
    """

    try:
        _is_lazy = is_lazy(argval)
    except:  # noqa
        return argval
    else:
        if _is_lazy:
            return argval.get(request_or_item)
        else:
            return argval


def get_test_node(request_or_item):
    """
    Return the test node, typically a _pytest.Function.
    Provided arg may be the node already, or the pytest request

    :param request_or_item:
    :return:
    """
    try:
        return request_or_item.node
    except AttributeError:
        return request_or_item
