# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
# Use true division operator always even in old python 2.x (used in `_extract_cases_from_module`)
from __future__ import division

from collections import namedtuple

import functools
from importlib import import_module
from inspect import getmembers, ismodule
import re
from warnings import warn

try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature  # noqa

try:
    from typing import Union, Callable, Iterable, Any, Type, List, Tuple  # noqa
except ImportError:
    pass

from .common_mini_six import string_types
from .common_others import get_code_first_line, AUTO, qname, funcopy, needs_binding, get_function_host, \
    in_same_module, get_host_module, get_class_that_defined_method
from .common_pytest_marks import copy_pytest_marks, make_marked_parameter_value, remove_pytest_mark, filter_marks, \
    get_param_argnames_as_list, Mark
from .common_pytest_lazy_values import LazyValue, LazyTuple, LazyTupleItem
from .common_pytest import safe_isclass, MiniMetafunc, is_fixture, get_fixture_name, inject_host, add_fixture_params, \
    list_all_fixtures_in, get_pytest_request_and_item, safe_isinstance

from .case_funcs import matches_tag_query, is_case_function, is_case_class, CASE_PREFIX_FUN, copy_case_info, \
    get_case_id, get_case_marks, GEN_BY_US

from .fixture_core1_unions import USED, NOT_USED
from .fixture_core2 import CombinedFixtureParamValue, fixture
from .fixture__creation import check_name_available, get_caller_module, CHANGE
from .fixture_parametrize_plus import fixture_ref, _parametrize_plus, FixtureParamAlternative, ParamAlternative, \
    SingleParamAlternative, MultiParamAlternative, FixtureRefItem

try:
    ModuleNotFoundError
except NameError:
    # python < 3.6
    ModuleNotFoundError = ImportError


THIS_MODULE = object()
"""Singleton that can be used instead of a module name to indicate that the module is the current one"""

try:
    from typing import Literal, Optional  # noqa
    from types import ModuleType  # noqa

    ModuleRef = Union[str, ModuleType, Literal[AUTO], Literal[THIS_MODULE]]  # noqa
    CaseType = Union[Callable, Type, ModuleRef]

except:  # noqa
    pass


_HOST_CLS_ATTR = '_pytestcases_host_cls'


def parametrize_with_cases(argnames,                # type: Union[str, List[str], Tuple[str, ...]]
                           cases=AUTO,              # type: Union[CaseType, List[CaseType]]
                           prefix=CASE_PREFIX_FUN,  # type: str
                           glob=None,               # type: str
                           has_tag=None,            # type: Any
                           filter=None,             # type: Callable[..., bool]  # noqa
                           ids=None,                # type: Union[Callable, Iterable[str]]
                           idstyle=None,            # type: Union[str, Callable]
                           # idgen=_IDGEN,            # type: Union[str, Callable]
                           debug=False,             # type: bool
                           scope="function",        # type: str
                           import_fixtures=False    # type: bool
                           ):
    # type: (...) -> Callable[[Callable], Callable]
    """
    A decorator for test functions or fixtures, to parametrize them based on test cases. It works similarly to
    `@pytest.mark.parametrize`: argnames represent a coma-separated string of arguments to inject in the decorated
    test function or fixture. The argument values (argvalues in `pytest.mark.parametrize`) are collected from the
    various case functions found according to `cases`, and injected as lazy values so that the case functions are called
    just before the test or fixture is executed.

    By default (`cases=AUTO`) the list of test cases is automatically drawn from the python module file named
    `test_<name>_cases.py` or if not found, `cases_<name>.py`, where `test_<name>` is the current module name.

    Finally, the `cases` argument also accepts an explicit case function, cases-containing class, module or module name;
    or a list of such elements. Note that both absolute and relative module names are suported.

    Note that `@parametrize_with_cases` collection and parameter creation steps are strictly equivalent to
    `get_all_cases` + `get_parametrize_args`. This can be handy for debugging purposes.

    ```python
    # Collect all cases
    cases_funs = get_all_cases(f, cases=cases, prefix=prefix, glob=glob, has_tag=has_tag, filter=filter)

    # Transform the various functions found
    argvalues = get_parametrize_args(host_class_or_module, cases_funs, debug=False)
    ```

    :param argnames: same than in @pytest.mark.parametrize
    :param cases: a case function, a class containing cases, a module object or a module name string (relative module
        names accepted). Or a list of such items. You may use `THIS_MODULE` or `'.'` to include current module.
        `AUTO` (default) means that the module named `test_<name>_cases.py` or if not found, `case_<name>.py`, will be
        loaded, where `test_<name>.py` is the module file of the decorated function. When a module is listed, all of
        its functions matching the `prefix`, `filter` and `has_tag` are selected, including those functions nested in
        classes following naming pattern `*Case*`. Nested subclasses are taken into account, as long as they follow the
        `*Case*` naming pattern. When classes are explicitly provided in the list, they can have any name and do not
        need to follow this `*Case*` pattern.
    :param prefix: the prefix for case functions. Default is 'case_' but you might wish to use different prefixes to
        denote different kind of cases, for example 'data_', 'algo_', 'user_', etc.
    :param glob: an optional glob-like pattern for case ids, for example "*_success" or "*_failure". Note that this
        is applied on the case id, and therefore if it is customized through `@case(id=...)` it should be taken into
        account.
    :param has_tag: a single tag or a tuple, set, list of tags that should be matched by the ones set with the `@case`
        decorator on the case function(s) to be selected.
    :param filter: a callable receiving the case function and returning `True` or a truth value in case the function
        needs to be selected.
    :param ids: optional custom ids, similar to the one in `pytest.mark.parametrize`. Users may either provide an
        iterable of string ids, or a callable. If a callable is provided it will receive the case functions. Users
        may wish to use `get_case_id` or other functions in the API to inspect the case functions.
    :param idstyle: This is mostly for debug. Style of ids to be used in the "union" fixtures generated by
        `@parametrize` if some cases are transformed into fixtures behind the scenes. `idstyle` possible values are
        'compact', 'explicit' or None/'nostyle' (default), or a callable. `idstyle` has no effect if no cases are
        transformed into fixtures. As opposed to `ids`, a callable provided here will receive a `ParamAlternative`
        object indicating which generated fixture should be used. See `@parametrize` for details.
    :param scope: the scope of the union fixture to create if `fixture_ref`s are found in the argvalues
    :param import_fixtures: experimental feature. Turn this to True in order to automatically import all fixtures
        defined in the cases module into the current module.
    :param debug: a boolean flag to debug what happens behind the scenes
    :return:
    """
    @inject_host
    def _apply_parametrization(f, host_class_or_module):
        """ execute parametrization of test function or fixture `f` """

        # Collect all cases
        cases_funs = get_all_cases(f, cases=cases, prefix=prefix, glob=glob, has_tag=has_tag, filter=filter)

        # Build ids from callable if provided.
        _ids = ids
        if ids is not None:
            try:
                # if this is an iterable, don't do anything
                iter(ids)
            except TypeError:
                # id this is a callable however, use the callable on the case function (not fixture_ref and lazy_values)
                _ids = tuple(ids(_get_original_case_func(c)[0]) for c in cases_funs)

        # Transform the various case functions found into `lazy_value` (for case functions not requiring fixtures)
        # or `fixture_ref` (for case functions requiring fixtures - for them we create associated case fixtures in
        # `host_class_or_module`)
        argvalues = get_parametrize_args(host_class_or_module, cases_funs, prefix=prefix,
                                         import_fixtures=import_fixtures, debug=debug, scope=scope)

        # Finally apply parametrization - note that we need to call the private method so that fixture are created in
        # the right module (not here)
        _parametrize_with_cases, needs_inject = _parametrize_plus(argnames, argvalues, ids=_ids, idstyle=idstyle,
                                                                  debug=debug, scope=scope)

        if needs_inject:
            return _parametrize_with_cases(f, host_class_or_module)
        else:
            return _parametrize_with_cases(f)

    return _apply_parametrization


def _get_original_case_func(case_fun  # type: Callable
                            ):
    """

    :param case_fun:
    :return: the original case function, and a boolean indicating if it is different from the input
    """
    case_in_class = hasattr(case_fun, _HOST_CLS_ATTR)
    true_case_func = case_fun.func if case_in_class else case_fun
    return true_case_func, case_in_class


def create_glob_name_filter(glob_str  # type: str
                            ):
    """
    Creates a glob-like matcher for the name of case functions
    The only special character that is supported is `*` and it can not be
    escaped. However it can be used multiple times in an expression.

    :param glob_str: for example `*_success` or `*_*`
    :return:
    """
    # escape all special regex characters, then find the (escaped) stars and turn them into the regex star .*
    re_str = re.escape(glob_str).replace("\\*", ".*")
    # add "end" special regex char
    name_matcher = re.compile(re_str + "$")

    def _glob_name_filter(case_fun):
        case_fun_id = get_case_id(case_fun)
        assert case_fun_id is not None
        return name_matcher.match(case_fun_id)

    return _glob_name_filter


def get_all_cases(parametrization_target=None,  # type: Callable
                  cases=None,                   # type: Union[CaseType, List[CaseType]]
                  prefix=CASE_PREFIX_FUN,       # type: str
                  glob=None,                    # type: str
                  has_tag=None,                 # type: Union[str, Iterable[str]]
                  filter=None                   # type: Callable[[Callable], bool]  # noqa
                  ):
    # type: (...) -> List[Callable]
    """
    Lists all desired cases for a given `parametrization_target` (a test function or a fixture). This function may be
    convenient for debugging purposes. See `@parametrize_with_cases` for details on the parameters.

    :param parametrization_target: either an explicit module object or a function or None. If it's a function, it will
        use the module it is defined in. If None is given, it will just get the module it was called from.
    :param cases: a case function, a class containing cases, a module or a module name string (relative module
        names accepted). Or a list of such items. You may use `THIS_MODULE` or `'.'` to include current module.
        `AUTO` (default) means that the module named `test_<name>_cases.py` will be loaded, where `test_<name>.py` is
        the module file of the decorated function. `AUTO2` allows you to use the alternative naming scheme
        `case_<name>.py`. When a module is listed, all of its functions matching the `prefix`, `filter` and `has_tag`
        are selected, including those functions nested in classes following naming pattern `*Case*`. When classes are
        explicitly provided in the list, they can have any name and do not need to follow this `*Case*` pattern.
    :param prefix: the prefix for case functions. Default is 'case_' but you might wish to use different prefixes to
        denote different kind of cases, for example 'data_', 'algo_', 'user_', etc.
    :param glob: a matching pattern for case ids, for example `*_success` or `*_failure`. The only special character
        that can be used for now in this pattern is `*`, it can not be escaped, and it can be used several times in the
        same expression. The pattern should match the entire case id for the case to be selected. Note that this is
        applied on the case id, and therefore if it is customized through `@case(id=...)` it will be taken into
        account.
    :param has_tag: a single tag or a tuple, set, list of tags that should be matched by the ones set with the `@case`
        decorator on the case function(s) to be selected.
    :param filter: a callable receiving the case function and returning True or a truth value in case the function
        needs to be selected.
    """
    # Handle single elements
    if isinstance(cases, string_types):
        cases = (cases,)
    else:
        try:
            cases = tuple(cases)
        except TypeError:
            cases = (cases,)

    # validate prefix
    if not isinstance(prefix, str):
        raise TypeError("`prefix` should be a string, found: %r" % prefix)

    # validate glob and filter and merge them in a single tuple of callables
    filters = ()
    if glob is not None:
        if not isinstance(glob, string_types):
            raise TypeError("`glob` should be a string containing a glob-like pattern (not a regex).")

        filters += (create_glob_name_filter(glob),)
    if filter is not None:
        if not callable(filter):
            raise TypeError(
                "`filter` should be a callable starting in pytest-cases 0.8.0. If you wish to provide a single"
                " tag to match, use `has_tag` instead.")

        filters += (filter,)

    # parent package
    if parametrization_target is None:
        parametrization_target = get_caller_module()

    if ismodule(parametrization_target):
        caller_module_name = parametrization_target.__name__
    elif callable(parametrization_target):
        caller_module_name = getattr(parametrization_target, '__module__', None)
    else:
        raise ValueError("Can't handle parametrization_target=%s" % parametrization_target)

    parent_pkg_name = '.'.join(caller_module_name.split('.')[:-1]) if caller_module_name is not None else None

    # start collecting all cases
    cases_funs = []
    for c in cases:
        # load case or cases depending on type
        if safe_isclass(c):
            # class - do not check name, it was explicitly passed
            new_cases = extract_cases_from_class(c, case_fun_prefix=prefix, check_name=False)
            cases_funs += new_cases
        elif callable(c):
            # function
            if is_case_function(c, check_prefix=False):  # do not check prefix, it was explicitly passed
                # bind it automatically if needed (if unbound class method)
                shall_bind, bound_c = needs_binding(c, return_bound=True)
                cases_funs.append(bound_c)
            else:
                raise ValueError("Unsupported case function: %r" % c)
        else:
            # module
            if c is AUTO:
                # First try `test_<name>_cases.py` Then `case_<name>.py`
                c = import_default_cases_module(caller_module_name)

            elif c is THIS_MODULE or c == '.':
                c = caller_module_name

            new_cases = extract_cases_from_module(c, package_name=parent_pkg_name, case_fun_prefix=prefix)
            cases_funs += new_cases

    # filter last, for easier debugging (collection will be slightly less performant when a large volume of cases exist)
    return [c for c in cases_funs
            if matches_tag_query(c, has_tag=has_tag, filter=filters)]


def get_parametrize_args(host_class_or_module,    # type: Union[Type, ModuleType]
                         cases_funs,              # type: List[Callable]
                         prefix,                  # type: str
                         scope="function",        # type: str
                         import_fixtures=False,   # type: bool
                         debug=False              # type: bool
                         ):
    # type: (...) -> List[CaseParamValue]
    """
    Transforms a list of cases (obtained from `get_all_cases`) into a list of argvalues for `@parametrize`.
    Each case function `case_fun` is transformed into one or several `lazy_value`(s) or a `fixture_ref`:

     - If `case_fun` requires at least on fixture, a fixture will be created if not yet present, and a `fixture_ref`
       will be returned. The fixture will be created in `host_class_or_module`
     - If `case_fun` is a parametrized case, one `lazy_value` with a partialized version will be created for each
       parameter combination.
     - Otherwise, `case_fun` represents a single case: in that case a single `lazy_value` is returned.

    :param host_class_or_module: host of the parametrization target. A class or a module.
    :param cases_funs: a list of case functions, returned typically by `get_all_cases`
    :param prefix:
    :param scope:
    :param import_fixtures: experimental feature. Turn this to True in order to automatically import all fixtures
        defined in the cases module into the current module.
    :param debug: a boolean flag, turn it to True to print debug messages.
    :return:
    """
    return [c for _f in cases_funs for c in case_to_argvalues(host_class_or_module, _f, prefix, scope, import_fixtures,
                                                              debug)]


class CaseParamValue(object):
    """Common class for lazy values and fixture refs created from cases"""
    __slots__ = ()

    def get_case_id(self):
        raise NotImplementedError()

    def get_case_function(self, request):
        raise NotImplementedError()


class _LazyValueCaseParamValue(LazyValue, CaseParamValue):
    """A case that does not require any fixture is transformed into a `lazy_value` parameter
    when passed to @parametrize.

    We subclass it so that we can easily find back all parameter values that are cases
    """

    def get_case_id(self):
        return super(_LazyValueCaseParamValue, self).get_id()

    def get_case_function(self, request):
        return _get_original_case_func(self.valuegetter)[0]

    def as_lazy_tuple(self, nb_params):
        return _LazyTupleCaseParamValue(self, nb_params)


class _LazyTupleCaseParamValue(LazyTuple, CaseParamValue):
    """A case representing a tuple"""

    def get_case_id(self):
        return super(_LazyTupleCaseParamValue, self).get_id()

    def get_case_function(self, request):
        return _get_original_case_func(self._lazyvalue.valuegetter)[0]


class _FixtureRefCaseParamValue(fixture_ref, CaseParamValue):
    """A case that requires at least a fixture is transformed into a `fixture_ref` parameter
    when passed to @parametrize"""

    def get_case_id(self):
        return self.get_name_for_id()

    def get_case_function(self, request):
        # get the case function copy, or copy of the partial
        f = request._arg2fixturedefs[self.fixture][0].func

        # extract the actual original case
        return f.__origcasefun__


def case_to_argvalues(host_class_or_module,    # type: Union[Type, ModuleType]
                      case_fun,                # type: Callable
                      prefix,                  # type: str
                      scope,                   # type: str
                      import_fixtures=False,   # type: bool
                      debug=False              # type: bool
                      ):
    # type: (...) -> Tuple[CaseParamValue, ...]
    """Transform a single case into one or several `lazy_value`(s) or a `fixture_ref` to be used in `@parametrize`

    If `case_fun` requires at least on fixture, a fixture will be created if not yet present, and a `fixture_ref` will
    be returned.

    If `case_fun` is a parametrized case, one `lazy_value` with a partialized version will be created for each parameter
    combination.

    Otherwise, `case_fun` represents a single case: in that case a single `lazy_value` is returned.

    :param case_fun:
    :param import_fixtures: experimental feature. Turn this to True in order to automatically import all fixtures
        defined in the cases module into the current module.
    :return:
    """
    # get the id from the case function either added by the @case decorator, or default one.
    case_id = get_case_id(case_fun, prefix_for_default_ids=prefix)

    # get the list of all calls that pytest *would* have made for such a (possibly parametrized) function
    meta = MiniMetafunc(case_fun)

    if not meta.requires_fixtures and not meta.is_parametrized:
        # only retrieve the extra marks added with @case, since the others will be automatically retrieved by the
        # lazy_value.
        case_marks = get_case_marks(case_fun, as_decorators=True)

        # if not meta.is_parametrized:
        # single unparametrized case function
        if debug:
            case_fun_str = qname(case_fun.func if isinstance(case_fun, functools.partial) else case_fun)
            print("Case function %s > 1 lazy_value() with id %s and additional marks %s"
                  % (case_fun_str, case_id, case_marks))
        return (_LazyValueCaseParamValue(case_fun, id=case_id, marks=case_marks),)
        # else:
        #     THIS WAS A PREMATURE OPTIMIZATION WITH MANY SHORTCOMINGS. For example what if the case function is
        #     itself parametrized with lazy values ? Let's consider that a parametrized case should be a fixture,
        #     for now
        #
        #     # parametrized. create one version of the callable for each parametrized call
        #     # do not forget to merge the marks !
        #     if debug:
        #         case_fun_str = qname(case_fun.func if isinstance(case_fun, functools.partial) else case_fun)
        #         print("Case function %s > tuple of lazy_value() with ids %s and additional marks %s"
        #               % (case_fun_str, ["%s-%s" % (case_id, c.id) for c in meta._calls],
        #                  [case_marks + tuple(c.marks) for c in meta._calls]))
        #     return tuple(lazy_value(functools.partial(case_fun, **c.funcargs),
        #                             id="%s-%s" % (case_id, c.id), marks=case_marks + tuple(c.marks))
        #                  for c in meta._calls)
    else:
        # at least 1 required fixture (direct req or through @pytest.mark.usefixtures ), OR parametrized.

        # if meta.is_parametrized:
        #    # nothing to do, the parametrization marks are on the fixture to create so they will be taken into account

        # create or reuse a fixture in the host (pytest collector: module or class) of the parametrization target
        fix_name, remaining_marks = get_or_create_case_fixture(case_id, case_fun, host_class_or_module,
                                                               meta.fixturenames_not_in_sig, scope,
                                                               import_fixtures=import_fixtures, debug=debug)

        # reference that case fixture, and preserve the case id in the associated id whatever the generated fixture name
        argvalues = _FixtureRefCaseParamValue(fix_name, id=case_id)
        if debug:
            case_fun_str = qname(case_fun.func if isinstance(case_fun, functools.partial) else case_fun)
            print("Case function %s > fixture_ref(%r) with marks %s" % (case_fun_str, fix_name, remaining_marks))
        # return a lengh-1 tuple because there is a single case created
        return (make_marked_parameter_value((argvalues,), marks=remaining_marks) if remaining_marks else argvalues,)


def get_or_create_case_fixture(case_id,                # type: str
                               case_fun,               # type: Callable
                               target_host,            # type: Union[Type, ModuleType]
                               add_required_fixtures,  # type: Iterable[str]
                               scope,                  # type: str
                               import_fixtures=False,  # type: bool
                               debug=False             # type: bool
                               ):
    # type: (...) -> Tuple[str, Tuple[Mark]]
    """
    When case functions require fixtures, we want to rely on pytest to inject everything. Therefore
    we create a "case fixture" wrapping the case function. Since a case function may not be located in the same place
    than the symbol decorated with @parametrize_with_cases, we create that "case fixture" in the
    appropriate module/class (the host of the test/fixture function, `target_host`).

    If the case is parametrized, the parametrization marks are put on the created fixture.

    If the case has other marks, they are returned as the

    Note that we create a small cache in the module/class in order to reuse the created fixture corresponding
    to a case function if it was already required by a test/fixture in this host.

    :param case_id:
    :param case_fun:
    :param target_host:
    :param add_required_fixtures:
    :param import_fixtures: experimental feature. Turn this to True in order to automatically import all fixtures
        defined in the cases module into the current module.
    :param debug:
    :return: the newly created fixture name, and the remaining marks not applied
    """
    if is_fixture(case_fun):
        raise ValueError("A case function can not be decorated as a `@fixture`. This seems to be the case for"
                         " %s. If you did not decorate it but still see this error, please report this issue"
                         % case_fun)

    # source: detect a functools.partial wrapper created by us because of a host class
    true_case_func, case_in_class = _get_original_case_func(case_fun)
    true_case_func_host = get_function_host(true_case_func)

    # for checks
    orig_name = true_case_func.__name__
    orig_case = true_case_func

    # destination
    target_in_class = safe_isclass(target_host)
    fix_cases_dct, imported_fixtures_list = _get_fixture_cases(target_host)  # get our "storage unit" in this module

    # shortcut if the case fixture is already known/registered in target host
    try:
        fix_name, marks = fix_cases_dct[(true_case_func, scope)]
        if debug:
            print("Case function %s > Reusing fixture %r and marks %s" % (qname(true_case_func), fix_name, marks))
        return fix_name, marks
    except KeyError:
        pass

    # not yet known there. Create a new symbol in the target host :
    # we need a "free" fixture name, and a "free" symbol name
    existing_fixture_names = []
    # -- fixtures in target module or class should not be overridden
    existing_fixture_names += list_all_fixtures_in(target_host, recurse_to_module=False)
    # -- are there fixtures in source module or class ? should not be overridden too
    if not in_same_module(target_host, true_case_func_host):
        fixtures_in_cases_module = list_all_fixtures_in(true_case_func_host, recurse_to_module=False)
        if len(fixtures_in_cases_module) > 0:
            # EXPERIMENTAL we can try to import the fixtures into current module
            if import_fixtures:
                from_module = get_host_module(true_case_func_host)
                if from_module not in imported_fixtures_list:
                    for f in list_all_fixtures_in(true_case_func_host, recurse_to_module=False, return_names=False):
                        f_name = get_fixture_name(f)
                        if (f_name in existing_fixture_names) or (f.__name__ in existing_fixture_names):
                            raise ValueError("Cannot import fixture %r from %r as it would override an existing symbol "
                                             "in %r. Please set `@parametrize_with_cases(import_fixtures=False)`"
                                             "" % (f, from_module, target_host))
                        target_host_module = target_host if not target_in_class else get_host_module(target_host)
                        setattr(target_host_module, f.__name__, f)

                    imported_fixtures_list.append(from_module)

            # Fix the problem with  "case_foo(foo)" leading to the generated fixture having the same name
            existing_fixture_names += fixtures_in_cases_module

    def name_changer(name, i):
        return name + '_' * i

    # start with name = case_id and find a name that does not exist
    fix_name = check_name_available(target_host, extra_forbidden_names=existing_fixture_names, name=case_id,
                                    if_name_exists=CHANGE, name_changer=name_changer)

    if debug:
        print("Case function %s > Creating fixture %r in %s" % (qname(true_case_func), fix_name, target_host))

    if case_in_class:
        if target_in_class:
            # both in class: direct copy of the non-partialized version
            case_fun = funcopy(true_case_func)
        else:
            # case in class and target in module: use the already existing partialized version
            case_fun = funcopy(case_fun)
    else:
        if target_in_class:
            # case in module and target in class: create a static method
            case_fun = staticmethod(true_case_func)
        else:
            # none in class: direct copy
            case_fun = funcopy(true_case_func)

    # place the special attribute __origcasefun__ so that `_FixtureCase.get_case_function` can find it back
    case_fun.__origcasefun__ = true_case_func

    # handle @pytest.mark.usefixtures by creating a wrapper where the fixture is added to the signature
    if add_required_fixtures:
        # create a wrapper with an explicit requirement for the fixtures. TODO: maybe we should append and not prepend?
        case_fun = add_fixture_params(case_fun, add_required_fixtures)
        # remove the `usefixtures` mark: maybe we should leave it as it does no harm ?
        remove_pytest_mark(case_fun, "usefixtures")

    # set all parametrization marks on the case function
    # get the list of all marks on this case
    case_marks = get_case_marks(case_fun, concatenate_with_fun_marks=True)

    if case_marks:
        # remove all parametrization marks from this list since they will be handled here
        case_marks = filter_marks(case_marks, remove='parametrize')

    # create a new fixture from a copy of the case function, and place it on the target host
    new_fix = fixture(name=fix_name, scope=scope)(case_fun)
    # mark as generated by pytest-cases so that we skip it during cases collection
    setattr(new_fix, GEN_BY_US, True)
    setattr(target_host, fix_name, new_fix)

    # remember it for next time (one per scope)
    fix_cases_dct[(true_case_func, scope)] = fix_name, case_marks

    # check that we did not touch the original case
    assert not is_fixture(orig_case)
    assert orig_case.__name__ == orig_name

    return fix_name, case_marks


def _get_fixture_cases(module_or_class  # type: Union[ModuleType, Type]
                       ):
    """
    Returns our 'storage unit' in a module or class, used to remember the fixtures created from case functions.
    That way we can reuse fixtures already created for cases, in a given module/class.

    In addition, the host module of the class, or the module itself, is used to store a list of modules
    from where we imported fixtures already. This relates to the EXPERIMENTAL `import_fixtures=True` param.
    """
    if ismodule(module_or_class):
        # module: everything is stored in the same place
        try:
            cache, imported_fixtures_list = module_or_class._fixture_cases
        except AttributeError:
            cache = dict()
            imported_fixtures_list = []
            module_or_class._fixture_cases = (cache, imported_fixtures_list)
    else:
        # class: on class only the fixtures dict is stored
        try:
            cache = module_or_class._fixture_cases
        except AttributeError:
            cache = dict()
            module_or_class._fixture_cases = cache

        # grab the imported fixtures list from the module host
        _, imported_fixtures_list = _get_fixture_cases(get_host_module(module_or_class))

    return cache, imported_fixtures_list


def import_default_cases_module(test_module_name):
    """
    Implements the `module=AUTO` behaviour of `@parameterize_cases`.

    `test_module_name` will have the format "test_<module>.py", the associated python module "test_<module>_cases.py"
    will be loaded to load the cases.

    If "test_<module>_cases.py" module is not found it looks for the alternate file `cases_<module>.py`.

    :param test_module_name: the test module
    :return:
    """
    # First try `test_<name>_cases.py`
    cases_module_name1 = "%s_cases" % test_module_name

    try:
        cases_module = import_module(cases_module_name1)
    except ModuleNotFoundError:
        # Then try `case_<name>.py`
        parts = test_module_name.split('.')
        assert parts[-1][0:5] == 'test_'
        cases_module_name2 = "%s.cases_%s" % ('.'.join(parts[:-1]), parts[-1][5:])
        try:
            cases_module = import_module(cases_module_name2)
        except ModuleNotFoundError:
            # Nothing worked
            raise ValueError("Error importing test cases module to parametrize %r: unable to import AUTO "
                             "cases module %r nor %r. Maybe you wish to import cases from somewhere else ? In that case"
                             "please specify `cases=...`."
                             % (test_module_name, cases_module_name1, cases_module_name2))

    return cases_module


def hasinit(obj):
    init = getattr(obj, "__init__", None)
    if init:
        return init != object.__init__


def hasnew(obj):
    new = getattr(obj, "__new__", None)
    if new:
        return new != object.__new__


class CasesCollectionWarning(UserWarning):
    """
    Warning emitted when pytest cases is not able to collect a file or symbol in a module.
    """
    # Note: if we change this, then the symbol MUST be present in __init__ for import, see GH#249
    __module__ = "pytest_cases"


def extract_cases_from_class(cls,
                             check_name=True,
                             case_fun_prefix=CASE_PREFIX_FUN,
                             _case_param_factory=None
                             ):
    # type: (...) -> List[Callable]
    """

    :param cls:
    :param check_name:
    :param case_fun_prefix:
    :param _case_param_factory:
    :return:
    """
    if is_case_class(cls, check_name=check_name):
        # see from _pytest.python import pytest_pycollect_makeitem

        if hasinit(cls):
            warn(
                CasesCollectionWarning(
                    "cannot collect cases class %r because it has a "
                    "__init__ constructor"
                    % (cls.__name__, )
                )
            )
            return []
        elif hasnew(cls):
            warn(
                CasesCollectionWarning(
                    "cannot collect test class %r because it has a "
                    "__new__ constructor"
                    % (cls.__name__, )
                )
            )
            return []

        return _extract_cases_from_module_or_class(cls=cls, case_fun_prefix=case_fun_prefix,
                                                   _case_param_factory=_case_param_factory)
    else:
        return []


def extract_cases_from_module(module,                           # type: ModuleRef
                              package_name=None,                # type: str
                              case_fun_prefix=CASE_PREFIX_FUN,  # type: str
                              _case_param_factory=None
                              ):
    # type: (...) -> List[Callable]
    """
    Internal method used to create a list of case functions for all cases available from the given module.
    See `@cases_data`

    See also `_pytest.python.PyCollector.collect` and `_pytest.python.PyCollector._makeitem` and
    `_pytest.python.pytest_pycollect_makeitem`: we could probably do this in a better way in pytest_pycollect_makeitem

    :param module:
    :param package_name:
    :param _case_param_factory:
    :return:
    """
    # optionally import module if passed as module name string
    if isinstance(module, string_types):
        module = import_module(module, package=package_name)

    return _extract_cases_from_module_or_class(module=module, _case_param_factory=_case_param_factory,
                                               case_fun_prefix=case_fun_prefix)


def _extract_cases_from_module_or_class(module=None,                      # type: ModuleRef
                                        cls=None,                         # type: Type
                                        case_fun_prefix=CASE_PREFIX_FUN,  # type: str
                                        _case_param_factory=None
                                        ):
    """

    :param module:
    :param _case_param_factory:
    :return:
    """
    if not ((cls is None) ^ (module is None)):
        raise ValueError("Only one of cls or module should be provided")

    container = cls or module

    # We will gather all cases in the reference module and put them in this dict (line no, case)
    cases_dct = dict()

    # List members - only keep the functions from the module file (not the imported ones)
    if module is not None:
        def _of_interest(f):
            # check if the function is actually *defined* in this module (not imported from elsewhere)
            # Note: we used code.co_filename == module.__file__ in the past
            # but on some targets the file changes to a cached one so this does not work reliably,
            # see https://github.com/smarie/python-pytest-cases/issues/72
            try:
                return f.__module__ == module.__name__
            except:  # noqa
                return False
    else:
        def _of_interest(x):  # noqa
            return True

    for m_name, m in getmembers(container, _of_interest):
        if is_case_class(m):
            co_firstlineno = get_code_first_line(m)
            cls_cases = extract_cases_from_class(m, case_fun_prefix=case_fun_prefix,
                                                 _case_param_factory=_case_param_factory)
            for _i, _m_item in enumerate(cls_cases):
                gen_line_nb = co_firstlineno + (_i / len(cls_cases))
                cases_dct[gen_line_nb] = _m_item

        elif is_case_function(m, prefix=case_fun_prefix):
            try:
                # read pytest magic attribute "place_as" to make sure this is placed correctly
                m_for_placing = m.place_as
            except AttributeError:
                # nominal: get the first line of code
                co_firstlineno = get_code_first_line(m)
            else:
                # currently we only support replacing inside the same module
                if m_for_placing.__module__ != m.__module__:
                    raise ValueError("Unsupported value for 'place_as' special pytest attribute on case function %s: %s"
                                     ". Virtual placing in another module is not supported yet by pytest-cases."
                                     % (m, m_for_placing))
                co_firstlineno = get_code_first_line(m_for_placing)

            if cls is not None:
                if isinstance(cls.__dict__[m_name], (staticmethod, classmethod)):
                    # no need to partialize a 'self' argument
                    # BUT we'll need to recopy all marks from the holding class to the function
                    # so let's partialize the function to get a safely editable copy of it
                    new_m = functools.partial(m)

                else:
                    # Make sure that there is at least one argument
                    try:
                        s = signature(m)
                    except Exception:  # noqa
                        # ignore any error here, this is optional.
                        pass
                    else:
                        if len(s.parameters) < 1 or (tuple(s.parameters.keys())[0] != "self"):
                            raise TypeError("case method is missing 'self' argument but is not static: %s" % m)
                    # partialize the function to get one without the 'self' argument
                    new_m = functools.partial(m, cls())

                # Remember the host class. We'll later use this flag to remember that this is a partial.
                setattr(new_m, _HOST_CLS_ATTR, cls)
                # Recopy all metadata concerning the case function, since partial does not copy the __dict__ by default
                new_m.__name__ = m.__name__
                copy_case_info(m, new_m)
                copy_pytest_marks(m, new_m, override=True)
                m = new_m
                del new_m
                # Finally, propagate all marks from the holding case class to the case function
                copy_pytest_marks(cls, m, override=False)

            if _case_param_factory is None:
                # Nominal usage: put the case in the dictionary
                if co_firstlineno in cases_dct:
                    raise ValueError("Error collecting case functions, line number used by %r is already used by %r !"
                                     % (m, cases_dct[co_firstlineno]))
                cases_dct[co_firstlineno] = m
            else:
                # Legacy usage where the cases generators were expanded here and inserted with a virtual line no
                _case_param_factory(m, co_firstlineno, cases_dct)

    # convert into a list, taking all cases in order of appearance in the code (sort by source code line number)
    cases = [cases_dct[k] for k in sorted(cases_dct.keys())]

    return cases


def get_current_params(request_or_item):
    """
    Returns a dictionary containing all parameters for the currently active `pytest` item.
    """
    # (0) get pytest `request` and `item`
    item, request = get_pytest_request_and_item(request_or_item)

    # (1) pre-scan for MultiParamAlternatives to store map of fixturename -> argnames
    mp_fix_to_args = dict()
    try:
        param_items = dict(item.callspec.params)
    except AttributeError:
        return {}, {}, {}

    for argname_or_fixname, param_value in item.callspec.params.items():
        if isinstance(param_value, MultiParamAlternative):
            # remember that the fixture named `param_value.alternative_name` represents the multiparam
            mp_fix_to_args[param_value.alternative_name] = param_value.argnames, param_value.decorated
            # we can discard this intermediate param now, it is useless
            del param_items[argname_or_fixname]

    # (2) now extract all parameters available and their associated information
    test_fun = request.node.function
    results_testfun_and_unknown_fixtures = []
    results_known_fixtures = dict()
    results_known_fixtures_but_not_found = dict()
    for argname_or_fixname, param_value in param_items.items():
        # print(argname_or_fixturename, param_value)

        if param_value in (NOT_USED, USED):
            continue  # param induced by Fixture Union: ignore

        elif not safe_isinstance(param_value, CombinedFixtureParamValue):
            # (a) Parameters on a test function, or parameters on a fixture with a fixture_ref inside (other fixturegen)
            argnames, actual_value, parametrized = get_current_param(param_value, argname_or_fixname, mp_fix_to_args)
            # - In nominal, we receive each (argname, value) pair independently and argnames = (argname_or_fixturename,)
            # - If a @parametrize containing `fixture_ref`s is present, various new parameters are received and the
            # `argname_or_fixturename` does not represent something useful. In this case, `argnames` may have length > 1

            # Save each parameter one by one now
            for i, _argname in enumerate(argnames):
                _val = actual_value[i] if len(argnames) > 1 else actual_value
                if parametrized is None:
                    # we are not able to know if the parameter is for the test function or a fixture
                    results_testfun_and_unknown_fixtures.append((_argname, _val))
                elif _is_same_parametrized_target(parametrized, test_fun):
                    # the parameter is for the test function
                    results_testfun_and_unknown_fixtures.append((_argname, _val))
                else:
                    # we are able to know that the parameter is for a fixture, but can we find that fixture ?
                    try:
                        fixname = _find_fixture_name(parametrized)
                    except Exception:
                        # we can't find the fixture. add it to the dict of "not found"
                        #  this is probably related to the fact that this is a case function or a dynamically
                        #  created fixture
                        results_known_fixtures_but_not_found.setdefault(parametrized, []).append((_argname, _val))
                    else:
                        results_known_fixtures.setdefault(fixname, []).append((_argname, _val))
        else:
            # (b) (Combined) parameters on a fixture, except those including fixture_refs
            fixturename = argname_or_fixname
            # de-combine each distinct @parametrize that was made on that fixture
            for argnames, argvals in param_value.iterparams():
                # this is a single @parametrize(argnames, argvals)
                # note: do not iterate on the argvals but on the argnames, as argvals can be a LazyTuple
                for item, argname in enumerate(argnames):
                    value = argvals[item] if len(argnames) > 1 else argvals  # argvals is already unpacked if single
                    _name, actual_value, _target = get_current_param(value, fixturename, mp_fix_to_args)
                    # the parameter is for a fixture
                    # if argname != _names[0] or len(_names) > 1:
                    #     get_current_param(value, fixturename, mp_fix_to_args, test_fun_name)
                    #     raise ValueError("Please report")
                    results_known_fixtures.setdefault(fixturename, []).append((argname, actual_value))

    # process the lists to create the outputs
    # First, the test function params and the legacy pytest fixture params (if not hidden by names of fun params)
    tests_and_legacy_fix_results_dict = dict(results_testfun_and_unknown_fixtures)
    if len(tests_and_legacy_fix_results_dict) != len(results_testfun_and_unknown_fixtures):
        raise ValueError("Error: multiple values found for the same parameter. Please report this issue")

    # Then new style fixtures. since in some cases fixture names can conflict with param names, we use a separate dict.
    fixture_results_dict = dict()
    for fixture_name, results_list in results_known_fixtures.items():
        fixture_results_dct = dict(results_list)
        if len(fixture_results_dct) != len(results_list):
            raise ValueError("Error: multiple values found for the same fixture parameter. Please report this issue")
        fixture_results_dict[fixture_name] = fixture_results_dct

    # the remainder: fixtures that cant be found.
    results_unknown_dict = dict()
    for function, results_list in results_known_fixtures_but_not_found.items():
        fixture_results_dct = dict(results_list)
        if len(fixture_results_dct) != len(results_list):
            raise ValueError("Error: multiple values found for the same parameter. Please report this issue")
        results_unknown_dict[function] = fixture_results_dct

    return tests_and_legacy_fix_results_dict, fixture_results_dict, results_unknown_dict


def _is_same_parametrized_target(parametrized, test_fun):
    """

    :param parametrized:
    :param test_fun:
    :return:
    """
    return parametrized.__name__ == test_fun.__name__


def _find_fixture_name(parametrized):
    """
    Finds the actual fixture symbol whose implementation is this function.
    :param parametrized:
    :return:
    """
    container = get_class_that_defined_method(parametrized)
    if container is None:
        container = get_function_host(parametrized)

    parametrized_fixture = getattr(container, parametrized.__name__)

    return get_fixture_name(parametrized_fixture)


def get_current_param(value, argname_or_fixturename, mp_fix_to_args):
    """
    This function's primary role is to unpack the various parameter values (instances of `ParamAlternative`) created by
    @parametrize when a fixture reference is used in the parametrization.

    Returns the argnames, actual value, and parametrized fixture name if it can be known,
    associated with parameter value `value`.

    :param value:
    :param argname_or_fixturename:
    :param mp_fix_to_args:
    :return: (argnames, actual_value, paramztrized_fixname)
    """
    try:
        # (1) Does this parameter correspond to a fixture *generated* by a MultiParamAlternative ?
        # If so we already have its true argnames and parametrization target here, and the value is directly the param.
        argnames, parametrized = mp_fix_to_args[argname_or_fixturename]
        actual_value = value
    except KeyError:
        # (2) Is this parameter a ParamAlternative? (this happens when at least 1 param in the argvals is a fixture_ref)
        if safe_isinstance(value, ParamAlternative):
            # if isinstance(value, MultiParamAlternative):
            #     return False  # ignore silently, already handled in the pass before the main loop
            if isinstance(value, SingleParamAlternative):
                # extract the various info available
                parametrized = value.decorated
                # actual_id = value.get_alternative_id()
                argnames = value.argnames
                actual_value = value.argval
                if len(argnames) == 1 and not isinstance(value, FixtureParamAlternative):
                    actual_value = actual_value[0]
            else:
                raise TypeError("Unsupported type, please report: %r" % type(value))
        else:
            # (3) "normal" parameter: each (argname, value) pair is received independently
            argnames = (argname_or_fixturename,)
            parametrized = None
            actual_value = value

    return argnames, actual_value, parametrized


Case = namedtuple("Case", ("id", "func", "params"))


def get_current_cases(request_or_item):
    """
    Returns a dictionary containing all case parameters for the currently active `pytest` item.
    You can either pass the `pytest` item (available in some hooks) or the `request` (available in hooks, and also
    directly as a fixture).

    For each test function argument parametrized using a `@parametrize_with_case(<argname>, ...)` this dictionary
    contains an entry `{<argname>: (case_id, case_function, case_params)}`. If several argnames are parametrized this
    way, a dedicated entry will be present for each argname. The tuple is a `namedtuple` containing

     - `id` a string containing the actual case id constructed by `@parametrize_with_cases`.
     - `function` the original case function.
     - `params` a dictionary, containing the parameters of the case, if itself is parametrized. Note that if the
    case is parametrized with `@parametrize_with_cases`, the associated parameter value in the dictionary will also be
    `(actual_id, case_function, case_params)`.

    If a fixture parametrized with cases is active, the dictionary will contain an entry `{<fixturename>: <dct>}` where
    `<dct>` is a dictionary `{<argname>: (case_id, case_function, case_params)}`.

    To get more information on a case function, you can use `get_case_marks(f)`, `get_case_tags(f)`.
    You can also use `matches_tag_query` to check if a case function matches some expectations either concerning its id
    or its tags. See https://smarie.github.io/python-pytest-cases/#filters-and-tags

    Note that you can get the same contents directly by using the `current_cases` fixture.
    """
    # (0) get pytest `request` and `item`
    item, request = get_pytest_request_and_item(request_or_item)

    # (1) retrieve all parameters
    test_res_dict, fixture_results_dict, res_unkfix_dict = get_current_params(request_or_item)

    # multiple nesyed @parametrize with fixture refs might have created several wrappers. access the
    res_unkfix_dict2 = {_get_place_as(k): v for k, v in res_unkfix_dict.items()}

    # Now create the results containing the cases and their parameters only
    case_fixture_names_to_remove = set()

    def _do(name, value, dct, preserve=False):
        if safe_isinstance(value, LazyTupleItem):
            value = value.host._lazyvalue
        elif safe_isinstance(value, FixtureRefItem):
            value = value.host

        if safe_isinstance(value, CaseParamValue):
            # Case function
            case_func = value.get_case_function(request)

            # Case id
            # we cannot use `get_case_id` because we do not know the prefix that was used
            # case_id = get_case_id(case_func, prefix_for_default_ids=)
            case_id = value.get_case_id()

            # Case parameter(s)
            case_params_dct = {}
            if safe_isinstance(value, _FixtureRefCaseParamValue):
                casefixname = value.fixture
                if casefixname in fixture_results_dict:
                    # case is a fixture and is parametrized 1
                    case_fixture_names_to_remove.add(casefixname)
                    for _n, _v in fixture_results_dict[casefixname].items():
                        _do(_n, _v, case_params_dct, preserve=True)
                else:
                    case_impl_fun = _get_place_as(case_func)
                    try:
                        paramz = res_unkfix_dict2[case_impl_fun]
                    except KeyError:
                        # case is a fixture but is not parametrized
                        pass
                    else:
                        # case is a fixture and is parametrized 2
                        # it was harder to find its params because they did not directly link to the fixture
                        for _n, _v in paramz.items():
                            _do(_n, _v, case_params_dct, preserve=True)
            else:
                # case is not a fixture: it cannot possibly be parametrized
                pass

            # Finally fill the results
            dct[name] = Case(case_id, case_func, case_params_dct)

        elif preserve:
            # used in nested scenarii
            dct[name] = value

    cases_res_dict = dict()
    for name, value in test_res_dict.items():
        # fill the main dict
        _do(name, value, cases_res_dict)

    # use a separate dict as name conflicts might happen
    cases_res_dict_fixs = dict()
    for name, value in fixture_results_dict.items():
        # fill a dedicated subdict
        sub_dict = {}
        for n, v in value.items():
            _do(n, v, sub_dict)
        if len(sub_dict) > 0:
            cases_res_dict_fixs[name] = sub_dict

    # finally remove the case fixtures from the result dict
    for f in case_fixture_names_to_remove:
        try:
            del cases_res_dict_fixs[f]
        except KeyError:
            pass

    # merge the two - put the fixtures at the end
    for k, v in cases_res_dict_fixs.items():
        if k not in cases_res_dict:
            cases_res_dict[k] = v

    return cases_res_dict


def _get_place_as(f):
    while True:
        try:
            f = f.place_as
        except AttributeError:
            return f


def get_current_case_id(request_or_item,
                        argnames  # type: Union[Iterable[str], str]
                        ):
    """ DEPRECATED - use `get_current_cases` instead
    A helper function to return the current case id for a given `pytest` item (available in some hooks) or `request`
    (available in hooks, and also directly as a fixture).

    You need to provide the argname(s) used in the corresponding `@parametrize_with_cases` so that this method finds
    the right id.

    :param request_or_item:
    :param argnames:
    :return:
    """
    warn("`get_current_case_id` is DEPRECATED - please use the `current_cases` fixture instead, or `get_current_cases`")

    # process argnames
    if isinstance(argnames, string_types):
        argnames = get_param_argnames_as_list(argnames)

    # retrieve the correct id
    all_case_funcs = get_current_cases(request_or_item)
    return all_case_funcs[argnames[0]][0]


# Below is the beginning of a switch from our code scanning tool above to the same one than pytest.
# from .common_pytest import is_fixture, safe_isclass, compat_get_real_func, compat_getfslineno
#
#
# class PytestCasesWarning(UserWarning):
#     """
#     Bases: :class:`UserWarning`.
#
#     Base class for all warnings emitted by pytest cases.
#     """
#
#     __module__ = "pytest_cases"
#
#
# class PytestCasesCollectionWarning(PytestCasesWarning):
#     """
#     Bases: :class:`PytestCasesWarning`.
#
#     Warning emitted when pytest cases is not able to collect a file or symbol in a module.
#     """
#
#     __module__ = "pytest_cases"
#
#
# class CasesModule(object):
#     """
#     A collector for test cases
#     This is a very lightweight version of `_pytest.python.Module`,the pytest collector for test functions and classes.
#
#     See also pytest_collect_file and pytest_pycollect_makemodule hooks
#     """
#     __slots__ = 'obj'
#
#     def __init__(self, module):
#         self.obj = module
#
#     def collect(self):
#         """
#         A copy of pytest Module.collect (PyCollector.collect actually)
#         :return:
#         """
#         if not getattr(self.obj, "__test__", True):
#             return []
#
#         # NB. we avoid random getattrs and peek in the __dict__ instead
#         # (XXX originally introduced from a PyPy need, still true?)
#         dicts = [getattr(self.obj, "__dict__", {})]
#         for basecls in getmro(self.obj.__class__):
#             dicts.append(basecls.__dict__)
#         seen = {}
#         values = []
#         for dic in dicts:
#             for name, obj in list(dic.items()):
#                 if name in seen:
#                     continue
#                 seen[name] = True
#                 res = self._makeitem(name, obj)
#                 if res is None:
#                     continue
#                 if not isinstance(res, list):
#                     res = [res]
#                 values.extend(res)
#
#         def sort_key(item):
#             fspath, lineno, _ = item.reportinfo()
#             return (str(fspath), lineno)
#
#         values.sort(key=sort_key)
#         return values
#
#     def _makeitem(self, name, obj):
#         """ An adapted copy of _pytest.python.pytest_pycollect_makeitem """
#         if safe_isclass(obj):
#             if self.iscaseclass(obj, name):
#                 raise ValueError("Case classes are not yet supported: %r" % obj)
#         elif self.iscasefunction(obj, name):
#             # mock seems to store unbound methods (issue473), normalize it
#             obj = getattr(obj, "__func__", obj)
#             # We need to try and unwrap the function if it's a functools.partial
#             # or a functools.wrapped.
#             # We mustn't if it's been wrapped with mock.patch (python 2 only)
#             if not (isfunction(obj) or isfunction(compat_get_real_func(obj))):
#                 filename, lineno = compat_getfslineno(obj)
#                 warn_explicit(
#                     message=PytestCasesCollectionWarning(
#                         "cannot collect %r because it is not a function." % name
#                     ),
#                     category=None,
#                     filename=str(filename),
#                     lineno=lineno + 1,
#                 )
#             elif getattr(obj, "__test__", True):
#                 if isgeneratorfunction(obj):
#                     filename, lineno = compat_getfslineno(obj)
#                     warn_explicit(
#                         message=PytestCasesCollectionWarning(
#                             "cannot collect %r because it is a generator function." % name
#                         ),
#                         category=None,
#                         filename=str(filename),
#                         lineno=lineno + 1,
#                     )
#                 else:
#                     res = list(self._gencases(name, obj))
#                 outcome.force_result(res)
#
#     def iscasefunction(self, obj, name):
#         """Similar to PyCollector.istestfunction"""
#         if name.startswith("case_"):
#             if isinstance(obj, staticmethod):
#                 # static methods need to be unwrapped
#                 obj = getattr(obj, "__func__", False)
#             return (
#                 getattr(obj, "__call__", False)
#                 and not is_fixture(obj) is None
#             )
#         else:
#             return False
#
#     def iscaseclass(self, obj, name):
#         """Similar to PyCollector.istestclass"""
#         return name.startswith("Case")
#
#     def _gencases(self, name, funcobj):
#         # generate the case associated with a case function object.
#         # note: the original PyCollector._genfunctions has a "metafunc" mechanism here, we do not need it.
#         return []
#
#
