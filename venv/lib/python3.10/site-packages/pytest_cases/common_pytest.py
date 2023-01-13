# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from __future__ import division

import inspect
import sys
import os
from importlib import import_module

from makefun import add_signature_parameters, wraps

try:  # python 3.3+
    from inspect import signature, Parameter
except ImportError:
    from funcsigs import signature, Parameter  # noqa

from inspect import isgeneratorfunction, isclass

try:
    from typing import Union, Callable, Any, Optional, Tuple, Type, Iterable, Sized, List  # noqa
except ImportError:
    pass

import pytest
from _pytest.python import Metafunc

from .common_mini_six import string_types
from .common_others import get_function_host
from .common_pytest_marks import make_marked_parameter_value, get_param_argnames_as_list, \
    get_pytest_parametrize_marks, get_pytest_usefixture_marks, PYTEST3_OR_GREATER, PYTEST6_OR_GREATER, \
    PYTEST38_OR_GREATER, PYTEST34_OR_GREATER, PYTEST33_OR_GREATER, PYTEST32_OR_GREATER, PYTEST71_OR_GREATER
from .common_pytest_lazy_values import is_lazy_value, is_lazy


# A decorator that will work to create a fixture containing 'yield', whatever the pytest version, and supports hooks
if PYTEST3_OR_GREATER:
    def pytest_fixture(hook=None, **kwargs):
        def _decorate(f):
            # call hook if needed
            if hook is not None:
                f = hook(f)

            # create the fixture
            return pytest.fixture(**kwargs)(f)
        return _decorate
else:
    def pytest_fixture(hook=None, name=None, **kwargs):
        """Generator-aware pytest.fixture decorator for legacy pytest versions"""
        def _decorate(f):
            if name is not None:
                # 'name' argument is not supported in this old version, use the __name__ trick.
                f.__name__ = name

            # call hook if needed
            if hook is not None:
                f = hook(f)

            # create the fixture
            if isgeneratorfunction(f):
                return pytest.yield_fixture(**kwargs)(f)
            else:
                return pytest.fixture(**kwargs)(f)
        return _decorate


def pytest_is_running():
    """Return True if the current process is a pytest run

    See https://stackoverflow.com/questions/25188119/test-if-code-is-executed-from-within-a-py-test-session
    """
    if PYTEST32_OR_GREATER:
        return "PYTEST_CURRENT_TEST" in os.environ
    else:
        import re
        return any(re.findall(r'pytest|py.test', sys.argv[0]))


def remove_duplicates(lst):
    dset = set()
    # relies on the fact that dset.add() always returns None.
    return [item for item in lst
            if item not in dset and not dset.add(item)]


def is_fixture(fixture_fun  # type: Any
               ):
    """
    Returns True if the provided function is a fixture

    :param fixture_fun:
    :return:
    """
    try:
        fixture_fun._pytestfixturefunction  # noqa
        return True
    except AttributeError:
        # not a fixture ?
        return False


def list_all_fixtures_in(cls_or_module, return_names=True, recurse_to_module=False):
    """
    Returns a list containing all fixture names (or symbols if `return_names=False`)
    in the given class or module.

    Note that `recurse_to_module` can be used so that the fixtures in the parent
    module of a class are listed too.

    :param cls_or_module:
    :param return_names:
    :param recurse_to_module:
    :return:
    """
    res = [get_fixture_name(symb) if return_names else symb
           for n, symb in inspect.getmembers(cls_or_module, lambda f: inspect.isfunction(f) or inspect.ismethod(f))
           if is_fixture(symb)]

    if recurse_to_module and not inspect.ismodule(cls_or_module):
        # TODO currently this only works for a single level of nesting, we should use __qualname__ (py3) or .im_class
        host = import_module(cls_or_module.__module__)
        res += list_all_fixtures_in(host, recurse_to_module=True, return_names=return_names)

    return res


def safe_isclass(obj  # type: object
                 ):
    # type: (...) -> bool
    """Ignore any exception via isinstance on Python 3."""
    try:
        return isclass(obj)
    except Exception:  # noqa
        return False


def safe_isinstance(obj,  # type: object
                    cls):
    # type: (...) -> bool
    """Ignore any exception via isinstance"""
    try:
        return isinstance(obj, cls)
    except Exception:  # noqa
        return False


def assert_is_fixture(fixture_fun  # type: Any
                      ):
    """
    Raises a ValueError if the provided fixture function is not a fixture.

    :param fixture_fun:
    :return:
    """
    if not is_fixture(fixture_fun):
        raise ValueError("The provided fixture function does not seem to be a fixture: %s. Did you properly decorate "
                         "it ?" % fixture_fun)


def get_fixture_name(fixture_fun  # type: Union[str, Callable]
                     ):
    """
    Internal utility to retrieve the fixture name corresponding to the given fixture function.
    Indeed there is currently no pytest API to do this.

    Note: this function can receive a string, in which case it is directly returned.

    :param fixture_fun:
    :return:
    """
    if isinstance(fixture_fun, string_types):
        return fixture_fun
    assert_is_fixture(fixture_fun)
    try:  # pytest 3
        custom_fixture_name = fixture_fun._pytestfixturefunction.name  # noqa
    except AttributeError:
        try:  # pytest 2
            custom_fixture_name = fixture_fun.func_name  # noqa
        except AttributeError:
            custom_fixture_name = None

    if custom_fixture_name is not None:
        # there is a custom fixture name
        return custom_fixture_name
    else:
        obj__name = getattr(fixture_fun, '__name__', None)
        if obj__name is not None:
            # a function, probably
            return obj__name
        else:
            # a callable object probably
            return str(fixture_fun)


def get_fixture_scope(fixture_fun):
    """
    Internal utility to retrieve the fixture scope corresponding to the given fixture function .
    Indeed there is currently no pytest API to do this.

    :param fixture_fun:
    :return:
    """
    assert_is_fixture(fixture_fun)
    return fixture_fun._pytestfixturefunction.scope  # noqa
    # except AttributeError:
    #     # pytest 2
    #     return fixture_fun.func_scope


# ---------------- working on pytest nodes (e.g. Function)

def is_function_node(node):
    try:
        node.function  # noqa
        return True
    except AttributeError:
        return False


def get_parametrization_markers(fnode):
    """
    Returns the parametrization marks on a pytest Function node.
    :param fnode:
    :return:
    """
    if PYTEST34_OR_GREATER:
        return list(fnode.iter_markers(name="parametrize"))
    else:
        return list(fnode.parametrize)


def get_param_names(fnode):
    """
    Returns a list of parameter names for the given pytest Function node.
    parameterization marks containing several names are split

    :param fnode:
    :return:
    """
    p_markers = get_parametrization_markers(fnode)
    param_names = []
    for paramz_mark in p_markers:
        argnames = paramz_mark.args[0] if len(paramz_mark.args) > 0 else paramz_mark.kwargs['argnames']
        param_names += get_param_argnames_as_list(argnames)
    return param_names


# ---------- test ids utils ---------
def combine_ids(paramid_tuples):
    """
    Receives a list of tuples containing ids for each parameterset.
    Returns the final ids, that are obtained by joining the various param ids by '-' for each test node

    :param paramid_tuples:
    :return:
    """
    #
    return ['-'.join(pid for pid in testid) for testid in paramid_tuples]


def make_test_ids(global_ids, id_marks, argnames=None, argvalues=None, precomputed_ids=None):
    """
    Creates the proper id for each test based on (higher precedence first)

     - any specific id mark from a `pytest.param` (`id_marks`)
     - the global `ids` argument of pytest parametrize (`global_ids`)
     - the name and value of parameters (`argnames`, `argvalues`) or the precomputed ids(`precomputed_ids`)

    See also _pytest.python._idvalset method

    :param global_ids:
    :param id_marks:
    :param argnames:
    :param argvalues:
    :param precomputed_ids:
    :return:
    """
    if global_ids is not None:
        # overridden at global pytest.mark.parametrize level - this takes precedence.
        # resolve possibly infinite generators of ids here
        p_ids = resolve_ids(global_ids, argvalues, full_resolve=True)
    else:
        # default: values-based
        if precomputed_ids is not None:
            if argnames is not None or argvalues is not None:
                raise ValueError("Only one of `precomputed_ids` or argnames/argvalues should be provided.")
            p_ids = precomputed_ids
        else:
            p_ids = make_test_ids_from_param_values(argnames, argvalues)

    # Finally, local pytest.param takes precedence over everything else
    for i, _id in enumerate(id_marks):
        if _id is not None:
            p_ids[i] = _id
    return p_ids


def resolve_ids(ids,                # type: Optional[Union[Callable, Iterable[str]]]
                argvalues,          # type: Sized(Any)
                full_resolve=False  # type: bool
                ):
    # type: (...) -> Union[List[str], Callable]
    """
    Resolves the `ids` argument of a parametrized fixture.

    If `full_resolve` is False (default), iterable ids will be resolved, but not callable ids. This is useful if the
    `argvalues` have not yet been cleaned of possible `pytest.param` wrappers.

    If `full_resolve` is True, callable ids will be called using the argvalues, so the result is guaranteed to be a
    list.
    """
    try:
        # an explicit list or generator of ids ?
        iter(ids)
    except TypeError:
        # a callable to apply on the values
        if full_resolve:
            return [ids(v) for v in argvalues]
        else:
            # return the callable without resolving
            return ids
    else:
        # iterable.
        try:
            # a sized container ? (list, set, tuple)
            nb_ids = len(ids)
            # convert to list
            ids = list(ids)
        except TypeError:
            # a generator. Consume it
            ids = [id for id, v in zip(ids, argvalues)]
            nb_ids = len(ids)

        if nb_ids != len(argvalues):
            raise ValueError("Explicit list or generator of `ids` provided has a different length (%s) than the number "
                             "of argvalues (%s). Ids provided: %r" % (len(ids), len(argvalues), ids))
        return ids


def make_test_ids_from_param_values(param_names,
                                    param_values,
                                    ):
    """
    Replicates pytest behaviour to generate the ids when there are several parameters in a single `parametrize.
    Note that param_values should not contain marks.

    :param param_names:
    :param param_values:
    :return: a list of param ids
    """
    if isinstance(param_names, string_types):
        raise TypeError("param_names must be an iterable. Found %r" % param_names)

    nb_params = len(param_names)
    if nb_params == 0:
        raise ValueError("empty list provided")
    elif nb_params == 1:
        paramids = []
        for _idx, v in enumerate(param_values):
            _id = mini_idvalset(param_names, (v,), _idx)
            paramids.append(_id)
    else:
        paramids = []
        for _idx, vv in enumerate(param_values):
            if len(vv) != nb_params:
                raise ValueError("Inconsistent lenghts for parameter names and values: '%s' and '%s'"
                                 "" % (param_names, vv))
            _id = mini_idvalset(param_names, vv, _idx)
            paramids.append(_id)
    return paramids


# ---- ParameterSet api ---
# def analyze_parameter_set(pmark=None, argnames=None, argvalues=None, ids=None, check_nb=True):
#     """
#     analyzes a parameter set passed either as a pmark or as distinct
#     (argnames, argvalues, ids) to extract/construct the various ids, marks, and
#     values
#
#     See also pytest.Metafunc.parametrize method, that calls in particular
#     pytest.ParameterSet._for_parametrize and _pytest.python._idvalset
#
#     :param pmark:
#     :param argnames:
#     :param argvalues:
#     :param ids:
#     :param check_nb: a bool indicating if we should raise an error if len(argnames) > 1 and any argvalue has
#          a different length than len(argnames)
#     :return: ids, marks, values
#     """
#     if pmark is not None:
#         if any(a is not None for a in (argnames, argvalues, ids)):
#             raise ValueError("Either provide a pmark OR the details")
#         argnames = pmark.param_names
#         argvalues = pmark.param_values
#         ids = pmark.param_ids
#
#     # extract all parameters that have a specific configuration (pytest.param())
#     custom_pids, p_marks, p_values = extract_parameterset_info(argnames, argvalues, check_nb=check_nb)
#
#     # get the ids by merging/creating the various possibilities
#     p_ids = make_test_ids(argnames=argnames, argvalues=p_values, global_ids=ids, id_marks=custom_pids)
#
#     return p_ids, p_marks, p_values


def extract_parameterset_info(argnames, argvalues, check_nb=True):
    """

    :param argnames: the names in this parameterset
    :param argvalues: the values in this parameterset
    :param check_nb: a bool indicating if we should raise an error if len(argnames) > 1 and any argvalue has
         a different length than len(argnames)
    :return:
    """
    pids = []
    pmarks = []
    pvalues = []
    if isinstance(argnames, string_types):
        raise TypeError("argnames must be an iterable. Found %r" % argnames)
    nbnames = len(argnames)
    for v in argvalues:
        _pid, _pmark, _pvalue = extract_pset_info_single(nbnames, v)

        pids.append(_pid)
        pmarks.append(_pmark)
        pvalues.append(_pvalue)

        if check_nb and nbnames > 1 and (len(_pvalue) != nbnames):
            raise ValueError("Inconsistent number of values in pytest parametrize: %s items found while the "
                             "number of parameters is %s: %s." % (len(_pvalue), nbnames, _pvalue))

    return pids, pmarks, pvalues


def extract_pset_info_single(nbnames, argvalue):
    """Return id, marks, value"""
    if is_marked_parameter_value(argvalue):
        # --id
        _id = get_marked_parameter_id(argvalue)
        # --marks
        marks = get_marked_parameter_marks(argvalue)
        # --value(a tuple if this is a tuple parameter)
        argvalue = get_marked_parameter_values(argvalue, nbargs=nbnames)
        return _id, marks, argvalue[0] if nbnames == 1 else argvalue
    else:
        # normal argvalue
        return None, None, argvalue


try:  # pytest 3.x+
    from _pytest.mark import ParameterSet  # noqa

    def is_marked_parameter_value(v):
        return isinstance(v, ParameterSet)

    def get_marked_parameter_marks(v):
        return v.marks

    def get_marked_parameter_values(v, nbargs):
        """This always returns a tuple. nbargs is useful for pytest2 compatibility """
        return v.values

    def get_marked_parameter_id(v):
        return v.id

except ImportError:  # pytest 2.x
    from _pytest.mark import MarkDecorator

    # noinspection PyPep8Naming
    def ParameterSet(values,
                     id,  # noqa
                     marks):
        """ Dummy function (not a class) used only by `parametrize` """
        if id is not None:
            raise ValueError("This should not happen as `pytest.param` does not exist in pytest 2")

        # smart unpack is required for compatibility
        val = values[0] if len(values) == 1 else values
        nbmarks = len(marks)

        if nbmarks == 0:
            return val
        elif nbmarks > 1:
            raise ValueError("Multiple marks on parameters not supported for old versions of pytest")
        else:
            # decorate with the MarkDecorator
            return marks[0](val)

    def is_marked_parameter_value(v):
        return isinstance(v, MarkDecorator)

    def get_marked_parameter_marks(v):
        return [v]

    def get_marked_parameter_values(v, nbargs):
        """Returns a tuple containing the values"""

        # v.args[-1] contains the values.
        # see MetaFunc.parametrize in pytest 2 to be convinced :)

        # if v.name in ('skip', 'skipif'):
        if nbargs == 1:
            # the last element of args is not a tuple when there is a single arg.
            return (v.args[-1],)
        else:
            return v.args[-1]
        # else:
        #     raise ValueError("Unsupported mark")

    def get_marked_parameter_id(v):
        return v.kwargs.get('id', None)


def get_pytest_nodeid(metafunc):
    try:
        return metafunc.definition.nodeid
    except AttributeError:
        return "unknown"


try:
    # pytest 7+ : scopes is an enum
    from _pytest.scope import Scope

    def get_pytest_function_scopeval():
        return Scope.Function

    def has_function_scope(fixdef):
        return fixdef._scope is Scope.Function

    def set_callspec_arg_scope_to_function(callspec, arg_name):
        callspec._arg2scope[arg_name] = Scope.Function

except ImportError:
    try:
        # pytest 3+
        from _pytest.fixtures import scopes as pt_scopes
    except ImportError:
        # pytest 2
        from _pytest.python import scopes as pt_scopes

    # def get_pytest_scopenum(scope_str):
    #     return pt_scopes.index(scope_str)

    def get_pytest_function_scopeval():
        return pt_scopes.index("function")

    def has_function_scope(fixdef):
        return fixdef.scopenum == get_pytest_function_scopeval()

    def set_callspec_arg_scope_to_function(callspec, arg_name):
        callspec._arg2scopenum[arg_name] = get_pytest_function_scopeval()  # noqa


if PYTEST71_OR_GREATER:
    from _pytest.python import IdMaker  # noqa

    _idval = IdMaker([], [], None, None, None, None, None)._idval
    _idval_kwargs = dict()
else:
    from _pytest.python import _idval  # noqa

    if PYTEST6_OR_GREATER:
        _idval_kwargs = dict(idfn=None,
                             nodeid=None,  # item is not used in pytest(>=6.0.0) nodeid is only used by idfn
                             config=None  # if a config hook was available it would be used before this is called)
                             )
    elif PYTEST38_OR_GREATER:
        _idval_kwargs = dict(idfn=None,
                             item=None,  # item is only used by idfn
                             config=None  # if a config hook was available it would be used before this is called)
                             )
    else:
        _idval_kwargs = dict(idfn=None,
                             # config=None  # if a config hook was available it would be used before this is called)
                             )


def mini_idval(
        val,      # type: object
        argname,  # type: str
        idx,      # type: int
):
    """
    A simplified version of idval where idfn, item and config do not need to be passed.

    :param val:
    :param argname:
    :param idx:
    :return:
    """
    return _idval(val=val, argname=argname, idx=idx, **_idval_kwargs)


def mini_idvalset(argnames, argvalues, idx):
    """ mimic _pytest.python._idvalset but can handle lazyvalues used for tuples or args

    argvalues should not be a pytest.param (ParameterSet)
    This function returns a SINGLE id for a single test node
    """
    if len(argnames) > 1 and is_lazy(argvalues):
        # handle the case of LazyTuple used for several args
        return argvalues.get_id()

    this_id = [
        _idval(val, argname, idx=idx, **_idval_kwargs)
        for val, argname in zip(argvalues, argnames)
    ]
    return "-".join(this_id)


try:
    from _pytest.compat import getfuncargnames  # noqa
except ImportError:
    def num_mock_patch_args(function):
        """ return number of arguments used up by mock arguments (if any) """
        patchings = getattr(function, "patchings", None)
        if not patchings:
            return 0

        mock_sentinel = getattr(sys.modules.get("mock"), "DEFAULT", object())
        ut_mock_sentinel = getattr(sys.modules.get("unittest.mock"), "DEFAULT", object())

        return len(
            [p for p in patchings if not p.attribute_name and (p.new is mock_sentinel or p.new is ut_mock_sentinel)]
        )

    # noinspection SpellCheckingInspection
    def getfuncargnames(function, cls=None):
        """Returns the names of a function's mandatory arguments."""
        parameters = signature(function).parameters

        arg_names = tuple(
            p.name
            for p in parameters.values()
            if (
                    p.kind is Parameter.POSITIONAL_OR_KEYWORD
                    or p.kind is Parameter.KEYWORD_ONLY
            )
            and p.default is Parameter.empty
        )

        # If this function should be treated as a bound method even though
        # it's passed as an unbound method or function, remove the first
        # parameter name.
        if cls and not isinstance(cls.__dict__.get(function.__name__, None), staticmethod):
            arg_names = arg_names[1:]
        # Remove any names that will be replaced with mocks.
        if hasattr(function, "__wrapped__"):
            arg_names = arg_names[num_mock_patch_args(function):]
        return arg_names


class MiniFuncDef(object):
    __slots__ = ('nodeid',)

    def __init__(self, nodeid):
        self.nodeid = nodeid


class MiniMetafunc(Metafunc):
    # noinspection PyMissingConstructor
    def __init__(self, func):
        from .plugin import PYTEST_CONFIG  # late import to ensure config has been loaded by now

        self.config = PYTEST_CONFIG

        # self.config can be `None` if the same module is reloaded by another thread/process inside a test (parallelism)
        # In that case, a priori we are outside the pytest main runner so we can silently ignore, this
        # MetaFunc will not be used/read by anyone.
        # See https://github.com/smarie/python-pytest-cases/issues/242
        #
        # if self.config is None:
        #     if pytest_is_running():
        #             raise ValueError("Internal error - config has not been correctly loaded. Please report")

        self.function = func
        self.definition = MiniFuncDef(func.__name__)
        self._calls = []
        # non-default parameters
        self.fixturenames = getfuncargnames(func)
        # add declared used fixtures with @pytest.mark.usefixtures
        self.fixturenames_not_in_sig = [f for f in get_pytest_usefixture_marks(func) if f not in self.fixturenames]
        if self.fixturenames_not_in_sig:
            self.fixturenames = tuple(self.fixturenames_not_in_sig + list(self.fixturenames))
        # get parametrization marks
        self.pmarks = get_pytest_parametrize_marks(self.function)
        if self.is_parametrized:
            self.update_callspecs()
            # preserve order
            self.required_fixtures = tuple(f for f in self.fixturenames if f not in self._calls[0].funcargs)
        else:
            self.required_fixtures = self.fixturenames

    @property
    def is_parametrized(self):
        return len(self.pmarks) > 0

    @property
    def requires_fixtures(self):
        return len(self.required_fixtures) > 0

    def update_callspecs(self):
        """

        :return:
        """
        for pmark in self.pmarks:
            if len(pmark.param_names) == 1:
                if PYTEST3_OR_GREATER:
                    argvals = tuple(v if is_marked_parameter_value(v) else (v,) for v in pmark.param_values)
                else:
                    argvals = []
                    for v in pmark.param_values:
                        if is_marked_parameter_value(v):
                            newmark = MarkDecorator(v.markname, v.args[:-1] + ((v.args[-1],),), v.kwargs)
                            argvals.append(newmark)
                        else:
                            argvals.append((v,))
                    argvals = tuple(argvals)
            else:
                argvals = pmark.param_values
            self.parametrize(argnames=pmark.param_names, argvalues=argvals, ids=pmark.param_ids,
                             # use indirect = False and scope = 'function' to avoid having to implement complex patches
                             indirect=False, scope='function')

        if not PYTEST33_OR_GREATER:
            # fix the CallSpec2 instances so that the marks appear in an attribute "mark"
            # noinspection PyProtectedMember
            for c in self._calls:
                c.marks = list(c.keywords.values())


def add_fixture_params(func, new_names):
    """Creates a wrapper of the given function with additional arguments"""

    old_sig = signature(func)

    # prepend all new parameters if needed
    for n in new_names:
        if n in old_sig.parameters:
            raise ValueError("argument named %s already present in signature" % n)
    new_sig = add_signature_parameters(old_sig,
                                       first=[Parameter(n, kind=Parameter.POSITIONAL_OR_KEYWORD) for n in new_names])

    assert not isgeneratorfunction(func)

    # normal function with return statement
    @wraps(func, new_sig=new_sig)
    def wrapped_func(**kwargs):
        for n in new_names:
            kwargs.pop(n)
        return func(**kwargs)

    # else:
    #     # generator function (with a yield statement)
    #     @wraps(fixture_func, new_sig=new_sig)
    #     def wrapped_fixture_func(*args, **kwargs):
    #         request = kwargs['request'] if func_needs_request else kwargs.pop('request')
    #         if is_used_request(request):
    #             for res in fixture_func(*args, **kwargs):
    #                 yield res
    #         else:
    #             yield NOT_USED

    return wrapped_func


def get_callspecs(func):
    """
    Returns a list of pytest CallSpec objects corresponding to calls that should be made for this parametrized function.
    This mini-helper assumes no complex things (scope='function', indirect=False, no fixtures, no custom configuration)

    :param func:
    :return:
    """
    meta = MiniMetafunc(func)
    # meta.update_callspecs()
    # noinspection PyProtectedMember
    return meta._calls


def cart_product_pytest(argnames, argvalues):
    """
     - do NOT use `itertools.product` as it fails to handle MarkDecorators
     - we also unpack tuples associated with several argnames ("a,b") if needed
     - we also propagate marks

    :param argnames:
    :param argvalues:
    :return:
    """
    # transform argnames into a list of lists
    argnames_lists = [get_param_argnames_as_list(_argnames) if len(_argnames) > 0 else [] for _argnames in argnames]

    # make the cartesian product per se
    argvalues_prod = _cart_product_pytest(argnames_lists, argvalues)

    # flatten the list of argnames
    argnames_list = [n for nlist in argnames_lists for n in nlist]

    # apply all marks to the arvalues
    argvalues_prod = [make_marked_parameter_value(tuple(argvalues), marks=marks) if len(marks) > 0 else tuple(argvalues)
                      for marks, argvalues in argvalues_prod]

    return argnames_list, argvalues_prod


def _cart_product_pytest(argnames_lists, argvalues):
    result = []

    # first perform the sub cartesian product with entries [1:]
    sub_product = _cart_product_pytest(argnames_lists[1:], argvalues[1:]) if len(argvalues) > 1 else None

    # then do the final product with entry [0]
    for x in argvalues[0]:
        # handle x
        nb_names = len(argnames_lists[0])

        # (1) extract meta-info
        x_id, x_marks, x_value = extract_pset_info_single(nb_names, x)
        x_marks_lst = list(x_marks) if x_marks is not None else []
        if x_id is not None:
            raise ValueError("It is not possible to specify a sub-param id when using the new parametrization style. "
                             "Either use the traditional style or customize all ids at once in `idgen`")

        # (2) possibly unpack
        if nb_names > 1:
            # if lazy value, we have to do something
            if is_lazy_value(x_value):
                x_value_lst = x_value.as_lazy_items_list(nb_names)
            else:
                x_value_lst = list(x_value)
        else:
            x_value_lst = [x_value]

        # product
        if len(argvalues) > 1:
            for m, p in sub_product:
                # combine marks and values
                result.append((x_marks_lst + m, x_value_lst + p))
        else:
            result.append((x_marks_lst, x_value_lst))

    return result


def inject_host(apply_decorator):
    """
    A decorator for function with signature `apply_decorator(f, host)`, in order to inject 'host', the host of f.

    Since it is not entirely feasible to detect the host in python, my first implementation was a bit complex: it was
    returning an object with custom implementation of __call__ and __get__ methods, both reacting when pytest collection
    happens.

    That was very complex. Now we rely on an approximate but good enough alternative with `get_function_host`

    :param apply_decorator:
    :return:
    """
    # class _apply_decorator_with_host_tracking(object):
    #     def __init__(self, _target):
    #         # This is called when the decorator is applied on the target. Remember the target and result of paramz
    #         self._target = _target
    #         self.__wrapped__ = None
    #
    #     def __get__(self, obj, type_=None):
    #         """
    #         When the decorated test function or fixture sits in a cl
    #         :param obj:
    #         :param type_:
    #         :return:
    #         """
    #         # We now know that the parametrized function/fixture self._target sits in obj (a class or a module)
    #         # We can therefore apply our parametrization accordingly (we need a reference to this host container in
    #         # order to store fixtures there)
    #         if self.__wrapped__ is None:
    #             self.__wrapped__ = 1  # means 'pending', to protect against infinite recursion
    #             try:
    #                 self.__wrapped__ = apply_decorator(self._target, obj)
    #             except Exception as e:
    #                 traceback = sys.exc_info()[2]
    #                 reraise(BaseException, e.args, traceback)
    #
    #                 # path, lineno = get_fslocation_from_item(self)
    #                 # warn_explicit(
    #                 #     "Error parametrizing function %s : [%s] %s" % (self._target, e.__class__, e),
    #                 #     category=None,
    #                 #     filename=str(path),
    #                 #     lineno=lineno + 1 if lineno is not None else None,
    #                 # )
    #                 #
    #                 # @wraps(self._target)
    #                 # def _exc_raiser(*args, **kwargs):
    #                 #     raise e
    #                 # # remove this metadata otherwise pytest will unpack it
    #                 # del _exc_raiser.__wrapped__
    #                 # self.__wrapped__ = _exc_raiser
    #
    #         return self.__wrapped__
    #
    #     def __getattribute__(self, item):
    #         if item == '__call__':
    #             # direct call means that the parametrized function sits in a module. import it
    #             host_module = import_module(self._target.__module__)
    #
    #             # next time the __call__ attribute will be set so callable() will work
    #             self.__call__ = self.__get__(host_module)
    #             return self.__call__
    #         else:
    #             return object.__getattribute__(self, item)
    #
    # return _apply_decorator_with_host_tracking

    def apply(test_or_fixture_func):
        # approximate: always returns the module and not the class :(
        #
        # indeed when this is called, the function exists (and its qualname mentions the host class) but the
        # host class is not yet created in the module, so it is not found by our `get_class_that_defined_method`
        #
        # but still ... this is far less complex to debug than the above attempt and it does not yet have side effects..
        container = get_function_host(test_or_fixture_func)
        return apply_decorator(test_or_fixture_func, container)

    return apply


def get_pytest_request_and_item(request_or_item):
    """Return the `request` and `item` (node) from whatever is provided"""
    try:
        item = request_or_item.node
    except AttributeError:
        item = request_or_item
        request = item._request
    else:
        request = request_or_item

    return item, request
