# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
import sys

PY3 = sys.version_info[0] >= 3
PY34 = sys.version_info[0:2] >= (3, 4)

if PY3:
    string_types = str,
else:
    string_types = basestring,  # noqa


# if PY3:
#     def reraise(tp, value, tb=None):
#         try:
#             if value is None:
#                 value = tp()
#             else:
#                 # HACK to fix bug
#                 value = tp(*value)
#             if value.__traceback__ is not tb:
#                 raise value.with_traceback(tb)
#             raise value
#         finally:
#             value = None
#             tb = None
#
# else:
#     def exec_(_code_, _globs_=None, _locs_=None):
#         """Execute code in a namespace."""
#         if _globs_ is None:
#             frame = sys._getframe(1)
#             _globs_ = frame.f_globals
#             if _locs_ is None:
#                 _locs_ = frame.f_locals
#             del frame
#         elif _locs_ is None:
#             _locs_ = _globs_
#         exec("""exec _code_ in _globs_, _locs_""")
#
#     exec_("""def reraise(tp, value, tb=None):
#     try:
#         raise tp, value, tb
#     finally:
#         tb = None
# """)


# def with_metaclass(meta, *bases):
#     """Create a base class with a metaclass."""
#     # This requires a bit of explanation: the basic idea is to make a dummy
#     # metaclass for one level of class instantiation that replaces itself with
#     # the actual metaclass.
#     class metaclass(type):
#
#         def __new__(cls, name, this_bases, d):
#             return meta(name, bases, d)
#
#         @classmethod
#         def __prepare__(cls, name, this_bases):
#             return meta.__prepare__(name, bases)
#     return type.__new__(metaclass, 'temporary_class', (), {})
