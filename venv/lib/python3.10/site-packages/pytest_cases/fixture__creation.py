# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from __future__ import division

from inspect import getmodule, currentframe
from warnings import warn

try:
    # type hints, python 3+
    from typing import Callable, Any, Union, Iterable  # noqa
    from types import ModuleType  # noqa
except ImportError:
    pass

from .common_others import make_identifier


class ExistingFixtureNameError(ValueError):
    """
    Raised by `add_fixture_to_callers_module` when a fixture already exists in a module
    """
    def __init__(self, module, name, caller):
        self.module = module
        self.name = name
        self.caller = caller

    def __str__(self):
        return "Symbol `%s` already exists in module %s and therefore a corresponding fixture can not be created by " \
               "`%s`" % (self.name, self.module, self.caller)


RAISE = 0
WARN = 1
CHANGE = 2


def check_name_available(module,
                         name,                  # type: str
                         if_name_exists=RAISE,  # type: int
                         name_changer=None,     # type: Callable
                         caller=None,           # type: Callable[[Any], Any]
                         extra_forbidden_names=()  # type: Iterable[str]
                         ):
    """
    Routine to check that a name is not already in dir(module) + extra_forbidden_names.
    The `if_name_exists` argument allows users to specify what happens if a name exists already.

    `if_name_exists=CHANGE` allows users to ask for a new non-conflicting name to be found and returned.

    :param module: a module or a class. dir(module) + extra_forbidden_names is used as a reference of forbidden names
    :param name: proposed name, to check against existent names in module
    :param if_name_exists: policy to apply if name already exists in dir(module) + extra_forbidden_names
    :param name_changer: an optional custom name changer function for new names to be generated
    :param caller: for warning / error messages. Something identifying the caller
    :param extra_forbidden_names: a reference list of additional forbidden names that can be provided, in addition to
        dir(module)
    :return: a name that might be different if policy was CHANGE
    """
    new_name = make_identifier(name)
    if new_name != name:
        if if_name_exists is RAISE:
            raise ValueError("Proposed name is an invalid identifier: %s" % name)
        elif if_name_exists is WARN:
            warn("%s name was not a valid identifier, changed it to %s" % (name, new_name))
        name = new_name

    if name_changer is None:
        # default style for name changing. i starts with 1
        def name_changer(name, i):
            return name + '_%s' % i

    ref_list = dir(module) + list(extra_forbidden_names)

    if name in ref_list:
        if caller is None:
            caller = ''

        # Name already exists: act according to policy
        if if_name_exists is RAISE:
            raise ExistingFixtureNameError(module, name, caller)

        elif if_name_exists is WARN:
            warn("%s Overriding symbol %s in module %s" % (caller, name, module))

        elif if_name_exists is CHANGE:
            # find a non-used name in that module
            i = 1
            name2 = name_changer(name, i)
            while name2 in ref_list:
                i += 1
                name2 = name_changer(name, i)

            name = name2
        else:
            raise ValueError("invalid value for `if_name_exists`: %s" % if_name_exists)

    return name


def get_caller_module(frame_offset=1):
    # type: (...) -> ModuleType
    """ Return the module where the last frame belongs.

    :param frame_offset: an alternate offset to look further up in the call stack
    :return:
    """
    # grab context from the caller frame
    frame = _get_callerframe(offset=frame_offset)
    return getmodule(frame)


def _get_callerframe(offset=0):
    """ Return a frame in the call stack

    :param offset: an alternate offset to look further up in the call stack
    :return:
    """
    # inspect.stack is extremely slow, the fastest is sys._getframe or inspect.currentframe().
    # See https://gist.github.com/JettJones/c236494013f22723c1822126df944b12
    # frame = sys._getframe(2 + offset)
    frame = currentframe()
    for _ in range(2 + offset):
        frame = frame.f_back
    return frame
