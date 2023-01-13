# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
import functools
import inspect
from keyword import iskeyword
import makefun
from importlib import import_module
from inspect import findsource
import re

try:
    from typing import Union, Callable, Any, Optional, Tuple, Type  # noqa
except ImportError:
    pass

from .common_mini_six import string_types, PY3, PY34


def get_code_first_line(f):
    """
    Returns the source code associated to function or class f. It is robust to wrappers such as @lru_cache
    :param f:
    :return:
    """
    # todo maybe use inspect.unwrap instead?
    if hasattr(f, '__wrapped__'):
        return get_code_first_line(f.__wrapped__)
    elif hasattr(f, '__code__'):
        # a function
        return f.__code__.co_firstlineno
    else:
        # a class ?
        try:
            _, lineno = findsource(f)
            return lineno
        except:  # noqa
            raise ValueError("Cannot get code information for function or class %r" % f)


# Below is the beginning of a switch from our scanning code to the same one than pytest. See `case_parametrizer_new`
# from _pytest.compat import get_real_func as compat_get_real_func
#
# try:
#     from _pytest._code.source import getfslineno as compat_getfslineno
# except ImportError:
#     from _pytest.compat import getfslineno as compat_getfslineno

try:
    ExpectedError = Optional[Union[Type[Exception], str, Exception, Callable[[Exception], Optional[bool]]]]
    """The expected error in case failure is expected. An exception type, instance, or a validation function"""

    ExpectedErrorType = Optional[Type[BaseException]]
    ExpectedErrorPattern = Optional[re.Pattern]
    ExpectedErrorInstance = Optional[BaseException]
    ExpectedErrorValidator = Optional[Callable[[BaseException], Optional[bool]]]

except:  # noqa
    pass


def unfold_expected_err(expected_e  # type: ExpectedError
                        ):
    # type: (...) -> Tuple[ExpectedErrorType, ExpectedErrorPattern, ExpectedErrorInstance, ExpectedErrorValidator]
    """
    'Unfolds' the expected error `expected_e` to return a tuple of
     - expected error type
     - expected error representation pattern (a regex Pattern)
     - expected error instance
     - error validation callable

    If `expected_e` is an exception type, returns `expected_e, None, None, None`

    If `expected_e` is a string, returns `BaseException, re.compile(expected_e), None, None`

    If `expected_e` is an exception instance, returns `type(expected_e), None, expected_e, None`

    If `expected_e` is an exception validation function, returns `BaseException, None, None, expected_e`

    :param expected_e: an `ExpectedError`, that is, either an exception type, a regex string, an exception
        instance, or an exception validation function
    :return:
    """
    if type(expected_e) is type and issubclass(expected_e, BaseException):
        return expected_e, None, None, None

    elif isinstance(expected_e, string_types):
        return BaseException, re.compile(expected_e), None, None  # noqa

    elif issubclass(type(expected_e), Exception):
        return type(expected_e), None, expected_e, None

    elif callable(expected_e):
        return BaseException, None, None, expected_e

    raise ValueError("ExpectedNormal error should either be an exception type, an exception instance, or an exception "
                     "validation callable")


def assert_exception(expected    # type: ExpectedError
                     ):
    """
    A context manager to check that some bit of code raises an exception. Sometimes it might be more
    handy than `with pytest.raises():`.

    `expected` can be:

     - an expected error type, in which case `isinstance(caught, expected)` will be used for validity checking

     - an expected error representation pattern (a regex pattern string), in which case
       `expected.match(repr(caught))` will be used for validity checking

     - an expected error instance, in which case BOTH `isinstance(caught, type(expected))` AND
       `caught == expected` will be used for validity checking

     - an error validation callable, in which case `expected(caught) is not False` will be used for validity
       checking

    Upon failure, this raises an `ExceptionCheckingError` (a subclass of `AssertionError`)

    ```python
    # good type - ok
    with assert_exception(ValueError):
        raise ValueError()

    # good type - inherited - ok
    class MyErr(ValueError):
        pass
    with assert_exception(ValueError):
        raise MyErr()

    # no exception - raises ExceptionCheckingError
    with assert_exception(ValueError):
        pass

    # wrong type - raises ExceptionCheckingError
    with assert_exception(ValueError):
        raise TypeError()

    # good repr pattern - ok
    with assert_exception(r"ValueError\\('hello'[,]+\\)"):
        raise ValueError("hello")

    # good instance equality check - ok
    class MyExc(Exception):
        def __eq__(self, other):
            return vars(self) == vars(other)
    with assert_exception(MyExc('hello')):
        raise MyExc("hello")

    # good equality but wrong type - raises ExceptionCheckingError
    with assert_exception(MyExc('hello')):
        raise Exception("hello")
    ```

    :param expected: an exception type, instance, repr string pattern, or a callable
    """
    return AssertException(expected)


class ExceptionCheckingError(AssertionError):
    pass


class AssertException(object):
    """ An implementation of the `assert_exception` context manager"""

    __slots__ = ('expected_exception', 'err_type', 'err_ptrn', 'err_inst', 'err_checker')

    def __init__(self, expected_exception):
        # First see what we need to assert
        err_type, err_ptrn, err_inst, err_checker = unfold_expected_err(expected_exception)
        self.expected_exception = expected_exception
        self.err_type = err_type
        self.err_ptrn = err_ptrn
        self.err_inst = err_inst
        self.err_checker = err_checker

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # bad: no exception caught
            raise AssertionError("DID NOT RAISE any BaseException")

        # Type check
        if not isinstance(exc_val, self.err_type):
            raise ExceptionCheckingError("Caught exception %r is not an instance of expected type %r"
                                         % (exc_val, self.err_type))

        # Optional - pattern matching
        if self.err_ptrn is not None:
            if not self.err_ptrn.match(repr(exc_val)):
                raise ExceptionCheckingError("Caught exception %r does not match expected pattern %r"
                                             % (exc_val, self.err_ptrn))

        # Optional - Additional Exception instance check with equality
        if self.err_inst is not None:
            # note: do not use != because in python 2 that is not equivalent
            if not (exc_val == self.err_inst):
                raise ExceptionCheckingError("Caught exception %r does not equal expected instance %r"
                                             % (exc_val, self.err_inst))

        # Optional - Additional Exception instance check with custom checker
        if self.err_checker is not None:
            if self.err_checker(exc_val) is False:
                raise ExceptionCheckingError("Caught exception %r is not valid according to %r"
                                             % (exc_val, self.err_checker))

        # Suppress the exception since it is valid.
        # See https://docs.python.org/2/reference/datamodel.html#object.__exit__
        return True


AUTO = object()
"""Marker for automatic defaults"""


def get_host_module(a):
    """get the host module of a, or a if it is already a module"""
    if inspect.ismodule(a):
        return a
    else:
        return import_module(a.__module__)


def in_same_module(a, b):
    """Compare the host modules of a and b"""
    return get_host_module(a) == get_host_module(b)


def get_function_host(func, fallback_to_module=True):
    """
    Returns the module or class where func is defined. Approximate method based on qname but "good enough"

    :param func:
    :param fallback_to_module: if True and an HostNotConstructedYet error is caught, the host module is returned
    :return:
    """
    host = None
    try:
        host = get_class_that_defined_method(func)
    except HostNotConstructedYet:
        # ignore if `fallback_to_module=True`
        if not fallback_to_module:
            raise

    if host is None:
        host = get_host_module(func)

    return host


def needs_binding(f, return_bound=False):
    # type: (...) -> Union[bool, Tuple[bool, Callable]]
    """Utility to check if a function needs to be bound to be used """

    # detect non-callables
    if isinstance(f, staticmethod):
        # only happens if the method is provided as Foo.__dict__['b'], not as Foo.b
        # binding is really easy here: pass any class

        # no need for the actual class
        # bound = f.__get__(get_class_that_defined_method(f.__func__))

        # f.__func__ (python 3) or f.__get__(object) (py2 and py3) work
        return (True, f.__get__(object)) if return_bound else True

    elif isinstance(f, classmethod):
        # only happens if the method is provided as Foo.__dict__['b'], not as Foo.b
        if not return_bound:
            return True
        else:
            host_cls = get_class_that_defined_method(f.__func__)
            bound = f.__get__(host_cls, host_cls)
            return True, bound

    else:
        # note that for the two above cases callable(f) returns False !
        if not callable(f) and (PY3 or not inspect.ismethoddescriptor(f)):
            raise TypeError("`f` is not a callable !")

    if isinstance(f, functools.partial) or fixed_ismethod(f) or is_bound_builtin_method(f):
        # already bound, although TODO the functools.partial one is a shortcut that should be analyzed more deeply
        return (False, f) if return_bound else False

    else:
        # can be a static method, a class method, a descriptor...
        if not PY3:
            host_cls = getattr(f, "im_class", None)
            if host_cls is None:
                # defined outside a class: no need for binding
                return (False, f) if return_bound else False
            else:
                bound_obj = getattr(f, "im_self", None)
                if bound_obj is None:
                    # unbound method
                    if return_bound:
                        # bind it on an instance
                        return True, f.__get__(host_cls(), host_cls)  # functools.partial(f, host_cls())
                    else:
                        return True
                else:
                    # yes: already bound, no binding needed
                    return (False, f) if return_bound else False
        else:
            try:
                qname = f.__qualname__
            except AttributeError:
                return (False, f) if return_bound else False
            else:
                if qname == f.__name__:
                    # not nested - plain old function in a module
                    return (False, f) if return_bound else False
                else:
                    # NESTED in a class or a function or ...
                    qname_parts = qname.split(".")

                    # normal unbound method (since we already eliminated bound ones above with fixed_ismethod(f))
                    # or static method accessed on an instance or on a class (!)
                    # or descriptor-created method
                    # if "__get__" in qname_parts:
                    #     # a method generated by a descriptor - should be already bound but...
                    #     #
                    #     # see https://docs.python.org/3/reference/datamodel.html#object.__set_name__
                    #     # The attribute __objclass__ may indicate that an instance of the given type (or a subclass)
                    #     # is expected or required as the first positional argument
                    #     cls_needed = getattr(f, '__objclass__', None)
                    #     if cls_needed is not None:
                    #         return (True, functools.partial(f, cls_needed())) if return_bound else True
                    #     else:
                    #         return (False, f) if return_bound else False

                    if qname_parts[-2] == "<locals>":
                        # a function generated by another function. most probably does not require binding
                        # since `get_class_that_defined_method` does not support those (as PEP3155 states)
                        # we have no choice but to make this assumption.
                        return (False, f) if return_bound else False

                    else:
                        # unfortunately in order to detect static methods we have no choice: we need the host class
                        host_cls = get_class_that_defined_method(f)
                        if host_cls is None:
                            get_class_that_defined_method(f)  # for debugging, do it again
                            raise NotImplementedError("This case does not seem covered, please report")

                        # is it a static method (on instance or class, it is the same),
                        # an unbound classmethod, or an unbound method ?
                        # To answer we need to go back to the definition
                        func_def = inspect.getattr_static(host_cls, f.__name__)
                        # assert inspect.getattr(host_cls, f.__name__) is f
                        if isinstance(func_def, staticmethod):
                            return (False, f) if return_bound else False
                        elif isinstance(func_def, classmethod):
                            # unbound class method
                            if return_bound:
                                # bind it on the class
                                return True, f.__get__(host_cls, host_cls)  # functools.partial(f, host_cls)
                            else:
                                return True
                        else:
                            # unbound method
                            if return_bound:
                                # bind it on an instance
                                return True, f.__get__(host_cls(), host_cls)  # functools.partial(f, host_cls())
                            else:
                                return True


def is_static_method(cls, func_name, func=None):
    """ Adapted from https://stackoverflow.com/a/64436801/7262247

    indeed isinstance(staticmethod) does not work if the method is already bound

    :param cls:
    :param func_name:
    :param func: optional, if you have it already
    :return:
    """
    if func is not None:
        assert getattr(cls, func_name) is func

    return isinstance(inspect.getattr_static(cls, func_name), staticmethod)


def is_class_method(cls, func_name, func=None):
    """ Adapted from https://stackoverflow.com/a/64436801/7262247

    indeed isinstance(classmethod) does not work if the method is already bound

    :param cls:
    :param func_name:
    :param func: optional, if you have it already
    :return:
    """
    if func is not None:
        assert getattr(cls, func_name) is func

    return isinstance(inspect.getattr_static(cls, func_name), classmethod)


def is_bound_builtin_method(meth):
    """Helper returning True if meth is a bound built-in method"""
    return (inspect.isbuiltin(meth)
            and getattr(meth, '__self__', None) is not None
            and getattr(meth.__self__, '__class__', None))


class HostNotConstructedYet(Exception):
    """Raised by `get_class_that_defined_method` in the situation where the host class is not in the host module yet."""
    pass


if PY3:
    # this does not need fixing
    fixed_ismethod = inspect.ismethod

    def get_class_that_defined_method(meth):
        """from https://stackoverflow.com/a/25959545/7262247

        Improved to support nesting, and to raise an Exception if __qualname__ does
        not properly work (instead of returning None which may be misleading)

        And yes PEP3155 states that __qualname__ should be used for such introspection.
        See https://www.python.org/dev/peps/pep-3155/#rationale
        """
        if isinstance(meth, functools.partial):
            return get_class_that_defined_method(meth.func)

        if inspect.ismethod(meth) or is_bound_builtin_method(meth):
            for cls in inspect.getmro(meth.__self__.__class__):
                if meth.__name__ in cls.__dict__:
                    return cls
            meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing

        if inspect.isfunction(meth):
            host = inspect.getmodule(meth)
            host_part = meth.__qualname__.split('.<locals>', 1)[0]
            # note: the local part of qname is not walkable see https://www.python.org/dev/peps/pep-3155/#limitations
            for item in host_part.split('.')[:-1]:
                try:
                    host = getattr(host, item)
                except AttributeError:
                    # non-resolvable __qualname__
                    raise HostNotConstructedYet(
                        "__qualname__ is not resolvable, this can happen if the host class of this method "
                        "%r has not yet been created. PEP3155 does not seem to tell us what we should do "
                        "in this case." % meth
                    )
                if host is None:
                    raise ValueError("__qualname__ leads to `None`, this is strange and not PEP3155 compliant, please "
                                     "report")

            if isinstance(host, type):
                return host

        return getattr(meth, '__objclass__', None)  # handle special descriptor objects

else:
    def fixed_ismethod(f):
        """inspect.ismethod does not have the same contract in python 2: it returns True even for bound methods"""
        return hasattr(f, '__self__') and f.__self__ is not None

    def get_class_that_defined_method(meth):
        """from https://stackoverflow.com/a/961057/7262247

        Adapted to support partial
        """
        if isinstance(meth, functools.partial):
            return get_class_that_defined_method(meth.func)

        try:
            _mro = inspect.getmro(meth.im_class)
        except AttributeError:
            # no host class
            return None
        else:
            for cls in _mro:
                if meth.__name__ in cls.__dict__:
                    return cls
        return None


if PY3:
    def qname(func):
        return func.__qualname__
else:
    def qname(func):
        """'good enough' python 2 implementation of __qualname__"""
        try:
            hostclass = func.im_class
        except AttributeError:
            # no host class
            return "%s.%s" % (func.__module__, func.__name__)
        else:
            # host class: recurse (note that in python 2 nested classes do not have a way to know their parent class)
            return "%s.%s" % (qname(hostclass), func.__name__)


# if sys.version_info > (3, ):
def funcopy(f):
    """

    >>> def foo():
    ...     return 1
    >>> foo.att = 2
    >>> f = funcopy(foo)
    >>> f.att
    2
    >>> f()
    1

    """
    # see https://stackoverflow.com/a/6527746/7262247
    # and https://stackoverflow.com/a/13503277/7262247
    # apparently it is not possible to create an actual copy with copy() !
    # Use makefun.partial which preserves the parametrization marks (we need them)
    return makefun.partial(f)
    # fun = FunctionType(f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__)
    # fun.__dict__.update(f.__dict__)
    # fun = functools.update_wrapper(fun, f)
    # fun.__kwdefaults__ = f.__kwdefaults__
    # return fun
# else:
#     def funcopy(f):
#         fun = FunctionType(f.func_code, f.func_globals, name=f.func_name, argdefs=f.func_defaults,
#                            closure=f.func_closure)
#         fun.__dict__.update(f.__dict__)
#         fun = functools.update_wrapper(fun, f)
#         fun.__kwdefaults__ = f.__kwdefaults__
#         return fun


def robust_isinstance(o, cls):
    try:
        return isinstance(o, cls)
    except:  # noqa
        return False


def isidentifier(s  # type: str
                 ):
    """python 2+3 compliant <str>.isidentifier()"""
    try:
        return s.isidentifier()
    except AttributeError:
        return re.match("[a-zA-Z_]\\w*\\Z", s)


def make_identifier(name  # type: str
                    ):
    """Transform the given name into a valid python identifier"""
    if not isinstance(name, string_types):
        raise TypeError("name should be a string, found : %r" % name)

    if iskeyword(name) or (not PY3 and name == "None"):
        # reserved keywords: add an underscore
        name = name + "_"

    if isidentifier(name):
        return name
    elif len(name) == 0:
        # empty string
        return "_"
    else:
        # first remove any forbidden character (https://stackoverflow.com/a/3305731/7262247)
        # \W : matches any character that is not a word character
        new_name = re.sub("\\W+", '_', name)
        # then add a leading underscore if needed
        # ^(?=\\d) : matches any digit that would be at the beginning of the string
        if re.match("^(?=\\d)", new_name):
            new_name = "_" + new_name
        return new_name


if PY34:
    def replace_list_contents(the_list, new_contents):
        """Replaces the contents of a list"""
        the_list.clear()
        the_list.extend(new_contents)
else:
    def replace_list_contents(the_list, new_contents):
        """Replaces the contents of a list"""
        del the_list[:]
        the_list.extend(new_contents)
