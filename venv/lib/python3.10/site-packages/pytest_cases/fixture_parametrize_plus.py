# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from inspect import isgeneratorfunction
from warnings import warn


try:  # python 3.3+
    from inspect import signature, Parameter
except ImportError:
    from funcsigs import signature, Parameter  # noqa

try:
    from collections.abc import Iterable
except ImportError:  # noqa
    from collections import Iterable

try:
    from typing import Union, Callable, List, Any, Sequence, Optional, Type, Tuple, TypeVar  # noqa
    from types import ModuleType  # noqa

    T = TypeVar('T', bound=Union[Type, Callable])
except ImportError:
    pass

import pytest
from makefun import with_signature, remove_signature_parameters, add_signature_parameters, wraps

from .common_mini_six import string_types
from .common_others import AUTO, robust_isinstance, replace_list_contents
from .common_pytest_marks import has_pytest_param, get_param_argnames_as_list
from .common_pytest_lazy_values import is_lazy_value, get_lazy_args
from .common_pytest import get_fixture_name, remove_duplicates, mini_idvalset, is_marked_parameter_value, \
    extract_parameterset_info, ParameterSet, cart_product_pytest, mini_idval, inject_host, \
    get_marked_parameter_values, resolve_ids, get_marked_parameter_id, get_marked_parameter_marks, is_fixture, \
    safe_isclass

from .fixture__creation import check_name_available, CHANGE, WARN
from .fixture_core1_unions import InvalidParamsList, NOT_USED, UnionFixtureAlternative, _make_fixture_union, \
    _make_unpack_fixture, UnionIdMakers
from .fixture_core2 import _create_param_fixture, fixture


def _fixture_product(fixtures_dest,
                     name,                # type: str
                     fixtures_or_values,
                     fixture_positions,
                     scope="function",    # type: str
                     unpack_into=None,    # type: Iterable[str]
                     autouse=False,       # type: bool
                     hook=None,           # type: Callable[[Callable], Callable]
                     caller=None,         # type: Callable
                     **kwargs):
    """
    Internal implementation for fixture products created by pytest parametrize plus.

    :param fixtures_dest:
    :param name:
    :param fixtures_or_values:
    :param fixture_positions:
    :param idstyle:
    :param scope:
    :param ids:
    :param unpack_into:
    :param autouse:
    :param kwargs:
    :return:
    """
    # test the `fixtures` argument to avoid common mistakes
    if not isinstance(fixtures_or_values, (tuple, set, list)):
        raise TypeError("fixture_product: the `fixtures_or_values` argument should be a tuple, set or list")
    else:
        has_lazy_vals = any(is_lazy_value(v) for v in fixtures_or_values)

    _tuple_size = len(fixtures_or_values)

    # first get all required fixture names
    f_names = [None] * _tuple_size
    for f_pos in fixture_positions:
        # possibly get the fixture name if the fixture symbol was provided
        f = fixtures_or_values[f_pos]
        if isinstance(f, fixture_ref):
            f = f.fixture
        # and remember the position in the tuple
        f_names[f_pos] = get_fixture_name(f)

    # remove duplicates by making it an ordered set
    all_names = remove_duplicates((n for n in f_names if n is not None))
    if len(all_names) < 1:
        raise ValueError("Empty fixture products are not permitted")

    def _tuple_generator(request, all_fixtures):
        for i in range(_tuple_size):
            fix_at_pos_i = f_names[i]
            if fix_at_pos_i is None:
                # fixed value
                # note: wouldnt it be almost as efficient but more readable to *always* call handle_lazy_args?
                yield get_lazy_args(fixtures_or_values[i], request) if has_lazy_vals else fixtures_or_values[i]
            else:
                # fixture value
                yield all_fixtures[fix_at_pos_i]

    # then generate the body of our product fixture. It will require all of its dependent fixtures
    @with_signature("(request, %s)" % ', '.join(all_names))
    def _new_fixture(request, **all_fixtures):
        return tuple(_tuple_generator(request, all_fixtures))

    _new_fixture.__name__ = name

    # finally create the fixture per se.
    # WARNING we do not use pytest.fixture but fixture so that NOT_USED is discarded
    f_decorator = fixture(scope=scope, autouse=autouse, hook=hook, **kwargs)
    fix = f_decorator(_new_fixture)

    # Dynamically add fixture to caller's module as explained in https://github.com/pytest-dev/pytest/issues/2424
    check_name_available(fixtures_dest, name, if_name_exists=WARN, caller=caller)
    setattr(fixtures_dest, name, fix)

    # if unpacking is requested, do it here
    if unpack_into is not None:
        # note that as for fixture unions, we can not expose the `in_cls` parameter.
        # but there is an easy workaround if unpacking is needed: call unpack_fixture separately
        _make_unpack_fixture(fixtures_dest, argnames=unpack_into, fixture=name, hook=hook, in_cls=False)

    return fix


_make_fixture_product = _fixture_product
"""A readable alias for callers not using the returned symbol"""


class fixture_ref(object):  # noqa
    """
    A reference to a fixture, to be used in `@parametrize`.
    You can create it from a fixture name or a fixture object (function).
    """
    __slots__ = 'fixture', 'theoretical_size', '_id'

    def __init__(self,
                 fixture,  # type: Union[str, Callable]
                 id=None,  # type: str  # noqa
                 ):
        """

        :param fixture: the name of the fixture to reference, or the fixture function itself
        :param id: an optional custom id to override the fixture name in ids.
        """
        self.fixture = get_fixture_name(fixture)
        self._id = id
        self.theoretical_size = None  # we dont know yet, will be filled by @parametrize

    def get_name_for_id(self):
        """return the name to use in ids."""
        return self._id if self._id is not None else self.fixture

    def __str__(self):
        # used in mini_idval for example
        return self.get_name_for_id()

    def __repr__(self):
        if self._id is not None:
            return "fixture_ref<%s, id=%s>" % (self.fixture, self._id)
        else:
            return "fixture_ref<%s>" % self.fixture

    def _check_iterable(self):
        """Raise a TypeError if this fixture reference is not iterable, that is, it does not represent a tuple"""
        if self.theoretical_size is None:
            raise TypeError("This `fixture_ref` has not yet been initialized, so it cannot be unpacked/iterated upon. "
                            "This is not supposed to happen when a `fixture_ref` is used correctly, i.e. as an item in"
                            " the `argvalues` of a `@parametrize` decorator. Please check the documentation for "
                            "details.")
        if self.theoretical_size == 1:
            raise TypeError("This fixture_ref does not represent a tuple of arguments, it is not iterable")

    def __len__(self):
        self._check_iterable()
        return self.theoretical_size

    def __getitem__(self, item):
        """
        Returns an item in the tuple described by this fixture_ref.
        This is just a facade, a FixtureRefItem.
        Note: this is only used when a custom `idgen` is passed to @parametrized
        """
        self._check_iterable()
        return FixtureRefItem(self, item)


class FixtureRefItem(object):
    """An item in a fixture_ref when this fixture_ref is used as a tuple."""
    __slots__ = 'host', 'item'

    def __init__(self,
                 host,  # type: fixture_ref
                 item   # type: int
                 ):
        self.host = host
        self.item = item

    def __repr__(self):
        return "%r[%s]" % (self.host, self.item)


# Fix for https://github.com/smarie/python-pytest-cases/issues/71
# In order for pytest to allow users to import this symbol in conftest.py
# they should be declared as optional plugin hooks.
# A workaround otherwise would be to remove the 'pytest_' name prefix
# See https://github.com/pytest-dev/pytest/issues/6475
@pytest.hookimpl(optionalhook=True)
def pytest_parametrize_plus(*args,
                            **kwargs):
    warn("`pytest_parametrize_plus` and `parametrize_plus` are deprecated. Please use the new alias `parametrize`. "
         "See https://github.com/pytest-dev/pytest/issues/6475", category=DeprecationWarning, stacklevel=2)
    return parametrize(*args, **kwargs)


parametrize_plus = pytest_parametrize_plus


class ParamAlternative(UnionFixtureAlternative):
    """Defines an "alternative", used to parametrize a fixture union in the context of parametrize

    It is similar to a union fixture alternative, except that it also remembers the parameter argnames.
    They are used to generate the test id corresponding to this alternative. See `_get_minimal_id` implementations.
    `ParamIdMakers` overrides some of the idstyles in `UnionIdMakers` so as to adapt them to these `ParamAlternative`
    objects.
    """
    __slots__ = ('argnames', 'decorated')

    def __init__(self,
                 union_name,        # type: str
                 alternative_name,  # type: str
                 param_index,       # type: int
                 argnames,          # type: Sequence[str]
                 decorated          # type: Callable
                 ):
        """

        :param union_name: the name of the union fixture created by @parametrize to switch between param alternatives
        :param alternative_name: the name of the fixture created by @parametrize to represent this alternative
        :param param_index: the index of this parameter in the list of argvalues passed to @parametrize
        :param argnames: the list of parameter names in @parametrize
        :param decorated: the test function or fixture that this alternative refers to
        """
        super(ParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                               alternative_index=param_index)
        self.argnames = argnames
        self.decorated = decorated

    def get_union_id(self):
        return ("(%s)" % ",".join(self.argnames)) if len(self.argnames) > 1 else self.argnames[0]

    def get_alternative_idx(self):
        return "P%s" % self.alternative_index

    def get_alternative_id(self):
        """Subclasses should return the smallest id representing this parametrize fixture union alternative"""
        raise NotImplementedError()


class SingleParamAlternative(ParamAlternative):
    """alternative class for single parameter value"""
    __slots__ = 'argval', 'id'

    def __init__(self,
                 union_name,        # type: str
                 alternative_name,  # type: str
                 param_index,       # type: int
                 argnames,          # type: Sequence[str]
                 argval,            # type: Any
                 id,                # type: Optional[str]
                 decorated          # type: Callable
                 ):
        """
        :param union_name: the name of the union fixture created by @parametrize to switch between param alternatives
        :param alternative_name: the name of the fixture created by @parametrize to represent this alternative
        :param param_index: the index of this parameter in the list of argvalues passed to @parametrize
        :param argnames: the list of parameter names in @parametrize
        :param argval: the value used by this parameter
        """
        super(SingleParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                     param_index=param_index, argnames=argnames, decorated=decorated)
        self.argval = argval
        self.id = id

    def get_alternative_id(self):
        """Since this alternative has no further parametrization (simplification for 1-param alternative),
        we create here the equivalent of the id of the argvalue if it was used as a parameter"""
        if self.id is not None:
            # custom id from `@parametrize(ids=<callable_or_list>)`
            return self.id
        else:
            return mini_idvalset(self.argnames, self.argval, idx=self.alternative_index)

    @classmethod
    def create(cls,
               new_fixture_host,   # type: Union[Type, ModuleType]
               test_func,          # type: Callable
               param_union_name,   # type: str
               argnames,           # type: Sequence[str]
               i,                  # type: int
               argvalue,           # type: Any
               id,                 # type: Union[str, Callable]
               hook=None,          # type: Callable
               debug=False         # type: bool
               ):
        # type: (...) -> SingleParamAlternative
        """
        Creates an alternative for fixture union `param_union_name`, to handle single parameter value
        argvalue = argvalues[i] in @parametrize.

        This alternative will refer to a newly created fixture in `new_fixture_host`, that will return `argvalue`.

        :param new_fixture_host: host (class, module) where the new fixture should be created
        :param test_func:
        :param param_union_name:
        :param argnames:
        :param i:
        :param argvalue: a (possibly marked with pytest.param) argvalue
        :param hook:
        :param debug:
        :return:
        """
        nb_params = len(argnames)
        param_names_str = '_'.join(argnames).replace(' ', '')

        # Create a unique fixture name
        p_fix_name = "%s_%s_P%s" % (test_func.__name__, param_names_str, i)
        p_fix_name = check_name_available(new_fixture_host, p_fix_name, if_name_exists=CHANGE, caller=parametrize)

        if debug:
            print(" - Creating new fixture %r to handle parameter %s" % (p_fix_name, i))

        # Now we'll create the fixture that will return the unique parameter value
        # since this parameter is unique, we do not parametrize the fixture (_create_param_fixture "auto_simplify" flag)
        # for this reason the possible pytest.param ids and marks have to be set somewhere else: we move them
        # to the alternative.

        # unwrap possible pytest.param on the argvalue to move them on the SingleParamAlternative
        has_pytestparam_wrapper = is_marked_parameter_value(argvalue)
        if has_pytestparam_wrapper:
            p_id = get_marked_parameter_id(argvalue)
            p_marks = get_marked_parameter_marks(argvalue)
            argvalue = get_marked_parameter_values(argvalue, nbargs=nb_params)
            if nb_params == 1:
                argvalue = argvalue[0]

        # Create the fixture. IMPORTANT auto_simplify=True : we create a NON-parametrized fixture.
        _create_param_fixture(new_fixture_host, argname=p_fix_name, argvalues=(argvalue,),
                              hook=hook, auto_simplify=True, debug=debug)

        # Create the alternative
        argvals = (argvalue,) if nb_params == 1 else argvalue
        p_fix_alt = SingleParamAlternative(union_name=param_union_name, alternative_name=p_fix_name,
                                           argnames=argnames, param_index=i, argval=argvals, id=id,
                                           decorated=test_func)

        # Finally copy the custom id/marks on the ParamAlternative if any
        if has_pytestparam_wrapper:
            p_fix_alt = ParameterSet(values=(p_fix_alt,), id=p_id, marks=p_marks)  # noqa

        return p_fix_alt


class MultiParamAlternative(ParamAlternative):
    """alternative class for multiple parameter values"""
    __slots__ = 'param_index_from', 'param_index_to'

    def __init__(self,
                 union_name,        # type: str
                 alternative_name,  # type: str
                 argnames,          # type: Sequence[str]
                 param_index_from,  # type: int
                 param_index_to,    # type: int
                 decorated          # type: Callable
                 ):
        """

        :param union_name: the name of the union fixture created by @parametrize to switch between param alternatives
        :param alternative_name: the name of the fixture created by @parametrize to represent this alternative
        :param argnames: the list of parameter names in @parametrize
        :param param_index_from: the beginning index of the parameters covered by <alternative_name> in the list of
            argvalues passed to @parametrize
        :param param_index_to: the ending index of the parameters covered by <alternative_name> in the list of
            argvalues passed to @parametrize
        """
        # set the param_index to be None since here we represent several indices
        super(MultiParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                    argnames=argnames, param_index=None, decorated=decorated  # noqa
                                                    )
        self.param_index_from = param_index_from
        self.param_index_to = param_index_to

    def __str__(self):
        return "%s/%s/" % (self.get_union_id(), self.get_alternative_idx())

    def get_alternative_idx(self):
        return "P%s:%s" % (self.param_index_from, self.param_index_to)

    def get_alternative_id(self):
        # The alternative id is the parameter range - the parameter themselves appear on the referenced fixture
        return self.get_alternative_idx()

    @classmethod
    def create(cls,
               new_fixture_host,  # type: Union[Type, ModuleType]
               test_func,         # type: Callable
               param_union_name,  # type: str
               argnames,          # type: Sequence[str]
               from_i,            # type: int
               to_i,              # type: int
               argvalues,         # type: Any
               ids,               # type: Union[Sequence[str], Callable]
               hook=None,         # type: Callable
               debug=False        # type: bool
               ):
        # type: (...) -> MultiParamAlternative
        """
        Creates an alternative for fixture union `param_union_name`, to handle a group of consecutive parameters
        argvalues[from_i:to_i] in @parametrize. Note that here the received `argvalues` should be already sliced

        This alternative will refer to a newly created fixture in `new_fixture_host`, that will be parametrized to
        return each of `argvalues`.

        :param new_fixture_host:
        :param test_func:
        :param param_union_name:
        :param argnames:
        :param from_i:
        :param to_i:
        :param argvalues:
        :param hook:
        :param debug:
        :return:
        """
        nb_params = len(argnames)
        param_names_str = '_'.join(argnames).replace(' ', '')

        # Create a unique fixture name
        p_fix_name = "%s_%s_is_P%stoP%s" % (test_func.__name__, param_names_str, from_i, to_i - 1)
        p_fix_name = check_name_available(new_fixture_host, p_fix_name, if_name_exists=CHANGE, caller=parametrize)

        if debug:
            print(" - Creating new fixture %r to handle parameters %s to %s" % (p_fix_name, from_i, to_i - 1))

        # Create the fixture
        # - it will be parametrized to take all the values in argvalues
        # - therefore it will use the custom ids and marks if any
        # - it will be unique (not unfolded) so if there are more than 1 argnames we have to add a layer of tuple in the
        #   values

        if nb_params > 1:
            # we have to create a tuple around the vals because we have a SINGLE parameter that is a tuple
            unmarked_argvalues = []
            new_argvals = []
            for v in argvalues:
                if is_marked_parameter_value(v):
                    # transform the parameterset so that it contains a tuple of length 1
                    vals = get_marked_parameter_values(v, nbargs=nb_params)
                    if nb_params == 1:
                        vals = vals[0]
                    unmarked_argvalues.append(vals)
                    new_argvals.append(ParameterSet((vals,),
                                                    id=get_marked_parameter_id(v),
                                                    marks=get_marked_parameter_marks(v)))
                else:
                    # nothing special to do since there is no pytest.param here
                    new_argvals.append(v)
                    unmarked_argvalues.append(v)
            argvalues = new_argvals

            # we also have to generate the ids correctly "as if they were multiple"
            try:
                iter(ids)
            except TypeError:
                if ids is not None:
                    ids = ["-".join(ids(vi) for vi in v) for v in unmarked_argvalues]
                else:
                    ids = [mini_idvalset(argnames, vals, i) for i, vals in enumerate(unmarked_argvalues)]

        _create_param_fixture(new_fixture_host, argname=p_fix_name, argvalues=argvalues, ids=ids, hook=hook,
                              debug=debug)

        # Create the corresponding alternative
        # note: as opposed to SingleParamAlternative, no need to move the custom id/marks to the ParamAlternative
        # since they are set on the created parametrized fixture above
        return MultiParamAlternative(union_name=param_union_name, alternative_name=p_fix_name, argnames=argnames,
                                     param_index_from=from_i, param_index_to=to_i, decorated=test_func)


class FixtureParamAlternative(SingleParamAlternative):
    """alternative class for a single parameter containing a fixture ref"""

    def __init__(self,
                 union_name,   # type: str
                 fixture_ref,  # type: fixture_ref
                 argnames,     # type: Sequence[str]
                 param_index,  # type: int
                 id,           # type: Optional[str]
                 decorated     # type: Callable
                 ):
        """
        :param union_name: the name of the union fixture created by @parametrize to switch between param alternatives
        :param param_index: the index of this parameter in the list of argvalues passed to @parametrize
        :param argnames: the list of parameter names in @parametrize
        :param fixture_ref: the fixture reference used in this alternative
        """
        # set alternative_name using the fixture name in fixture_ref
        super(FixtureParamAlternative, self).__init__(union_name=union_name,
                                                      alternative_name=fixture_ref.fixture,
                                                      argnames=argnames, param_index=param_index,
                                                      argval=fixture_ref, id=id, decorated=decorated)

    def get_alternative_idx(self):
        return "P%sF" % self.alternative_index

    def get_alternative_id(self):
        if self.id is not None:
            # custom id from `@parametrize(ids=<callable_or_list>)`
            return self.id
        else:
            # ask the fixture_ref for an id: it can be the fixture name or a custom id
            return self.argval.get_name_for_id()


class ProductParamAlternative(SingleParamAlternative):
    """alternative class for a single product parameter containing fixture refs"""

    def get_alternative_idx(self):
        return "P%sF" % self.alternative_index

    def get_alternative_id(self):
        """Similar to SingleParamAlternative: create an id representing this tuple, since the fixture wont be
        parametrized"""
        if self.id is not None:
            # custom id from `@parametrize(ids=<callable_or_list>)`
            return self.id
        else:
            argval = tuple(t if not robust_isinstance(t, fixture_ref) else t.get_name_for_id() for t in self.argval)
            return mini_idvalset(self.argnames, argval, idx=self.alternative_index)


# if PYTEST54_OR_GREATER:
#     # an empty string will be taken into account but NOT filtered out in CallSpec2.id.
#     # so instead we create a dedicated unique string and return it.
#     # Ugly but the only viable alternative seems worse: it would be to return an empty string
#     # and in `remove_empty_ids` to always remove all empty strings (not necessary the ones set by us).
#     # That is too much of a change.

EMPTY_ID = "<pytest_cases_empty_id>"


if has_pytest_param:
    def remove_empty_ids(callspec):
        # used by plugin.py to remove the EMPTY_ID from the callspecs
        replace_list_contents(callspec._idlist, [c for c in callspec._idlist if not c.startswith(EMPTY_ID)])
else:
    def remove_empty_ids(callspec):
        # used by plugin.py to remove the EMPTY_ID from the callspecs
        replace_list_contents(callspec._idlist, [c for c in callspec._idlist if not c.endswith(EMPTY_ID)])


# elif PYTEST421_OR_GREATER:
#     # an empty string will be taken into account and filtered out in CallSpec2.id.
#     # but.... if this empty string appears several times in the tests it is appended with a number to become unique :(
#     EMPTY_ID = ""
#
# else:
#     # an empty string will only be taken into account if its truth value is True
#     # but.... if this empty string appears several times in the tests it is appended with a number to become unique :(
#     # it will be filtered out in CallSpec2.id
#     class EmptyId(str):
#         def __new__(cls):
#             return str.__new__(cls, "")
#
#         def __nonzero__(self):
#             # python 2
#             return True
#
#         def __bool__(self):
#             # python 3
#             return True
#
#     EMPTY_ID = EmptyId()


class ParamIdMakers(UnionIdMakers):
    """ 'Enum' of id styles for param ids

    It extends UnionIdMakers to adapt to the special fixture alternatives `ParamAlternative` we create
    in @parametrize
    """
    @classmethod
    def nostyle(cls,
                param  # type: ParamAlternative
                ):
        if isinstance(param, MultiParamAlternative):
            # make an empty minimal id since the parameter themselves will appear as ids separately
            # note if the final id is empty it will be dropped by the filter in CallSpec2.id
            return EMPTY_ID
        else:
            return UnionIdMakers.nostyle(param)

    # @classmethod
    # def explicit(cls,
    #              param  # type: ParamAlternative
    #              ):
    #     """Same than parent but display the argnames as prefix instead of the fixture union name generated by
    #     @parametrize, because the latter is too complex (for unicity reasons)"""
    #     return "%s/%s" % (, param.get_id(prepend_index=True))


_IDGEN = object()


def parametrize(argnames=None,   # type: Union[str, Tuple[str], List[str]]
                argvalues=None,  # type: Iterable[Any]
                indirect=False,  # type: bool
                ids=None,        # type: Union[Callable, Iterable[str]]
                idstyle=None,    # type: Union[str, Callable]
                idgen=_IDGEN,    # type: Union[str, Callable]
                auto_refs=True,  # type: bool
                scope=None,      # type: str
                hook=None,       # type: Callable[[Callable], Callable]
                debug=False,     # type: bool
                **args):
    # type: (...) -> Callable[[T], T]
    """
    Equivalent to `@pytest.mark.parametrize` but also supports

    (1) new alternate style for argnames/argvalues. One can also use `**args` to pass additional `{argnames: argvalues}`
    in the same parametrization call. This can be handy in combination with `idgen` to master the whole id template
    associated with several parameters. Note that you can pass coma-separated argnames too, by de-referencing a dict:
    e.g. `**{'a,b': [(0, True), (1, False)], 'c': [-1, 2]}`.

    (2) new alternate style for ids. One can use `idgen` instead of `ids`. `idgen` can be a callable receiving all
    parameters at once (`**args`) and returning an id ; or it can be a string template using the new-style string
    formatting where the argnames can be used as variables (e.g. `idgen=lambda **args: "a={a}".format(**args)` or
    `idgen="my_id where a={a}"`). The special `idgen=AUTO` symbol can be used to generate a default string template
    equivalent to `lambda **args: "-".join("%s=%s" % (n, v) for n, v in args.items())`. This is enabled by default
    if you use the alternate style for argnames/argvalues (e.g. if `len(args) > 0`), and if there are no `fixture_ref`s
    in your argvalues.

    (3) new possibilities in argvalues:

     - one can include references to fixtures with `fixture_ref(<fixture>)` where <fixture> can be the fixture name or
       fixture function. When such a fixture reference is detected in the argvalues, a new function-scope "union"
       fixture will be created with a unique name, and the test function will be wrapped so as to be injected with the
       correct parameters from this fixture. Special test ids will be created to illustrate the switching between the
       various normal parameters and fixtures. You can see debug print messages about all fixtures created using
       `debug=True`

     - one can include lazy argvalues with `lazy_value(<valuegetter>, [id=..., marks=...])`. A `lazy_value` is the same
       thing than a function-scoped fixture, except that the value getter function is not a fixture and therefore can
       neither be parametrized nor depend on fixtures. It should have no mandatory argument.

    Both `fixture_ref` and `lazy_value` can be used to represent a single argvalue, or a whole tuple of argvalues when
    there are several argnames. Several of them can be used in a tuple.

    Finally, `pytest.param` is supported even when there are `fixture_ref` and `lazy_value`.

    An optional `hook` can be passed, to apply on each fixture function that is created during this call. The hook
    function will be called everytime a fixture is about to be created. It will receive a  single argument (the
    function implementing the fixture) and should return the function to use. For example you can use `saved_fixture`
    from `pytest-harvest` as a hook in order to save all such created fixtures in the fixture store.

    :param argnames: same as in pytest.mark.parametrize
    :param argvalues: same as in pytest.mark.parametrize except that `fixture_ref` and `lazy_value` are supported
    :param indirect: same as in pytest.mark.parametrize. Note that it is not recommended and is not guaranteed to work
        in complex parametrization scenarii.
    :param ids: same as in pytest.mark.parametrize. Note that an alternative way to create ids exists with `idgen`. Only
        one non-None `ids` or `idgen should be provided.
    :param idgen: an id formatter. Either a string representing a template, or a callable receiving all argvalues
        at once (as opposed to the behaviour in pytest ids). This alternative way to generate ids can only be used when
        `ids` is not provided (None). You can use the special `AUTO` formatter to generate an automatic id with
        template <name>=<value>-<name2>=<value2>-etc. `AUTO` is enabled by default if you use the alternate style for
        argnames/argvalues (e.g. if `len(args) > 0`), and if there are no `fixture_ref`s in your argvalues.
    :param auto_refs: a boolean. If this is `True` (default), argvalues containing fixture symbols will automatically
        be wrapped into a `fixture_ref`, for convenience.
    :param idstyle: This is mostly for debug. Style of ids to be used in the "union" fixtures generated by
        `@parametrize` if at least one `fixture_ref` is found in the argvalues. `idstyle` possible values are
        'compact', 'explicit' or None/'nostyle' (default), or a callable. `idstyle` has no effect if no `fixture_ref`
        are present in the argvalues. As opposed to `ids`, a callable provided here will receive a `ParamAlternative`
        object indicating which generated fixture should be used. See `ParamIdMakers`.
    :param scope: The scope of the union fixture to create if `fixture_ref`s are found in the argvalues. Otherwise same
        as in pytest.mark.parametrize.
    :param hook: an optional hook to apply to each fixture function that is created during this call. The hook function
        will be called everytime a fixture is about to be created. It will receive a single argument (the function
        implementing the fixture) and should return the function to use. For example you can use `saved_fixture` from
        `pytest-harvest` as a hook in order to save all such created fixtures in the fixture store.
    :param debug: print debug messages on stdout to analyze fixture creation (use pytest -s to see them)
    :param args: additional {argnames: argvalues} definition
    :return:
    """
    _decorate, needs_inject = _parametrize_plus(argnames, argvalues, indirect=indirect, ids=ids, idgen=idgen,
                                                auto_refs=auto_refs, idstyle=idstyle, scope=scope,
                                                hook=hook, debug=debug, **args)
    if needs_inject:
        @inject_host
        def _apply_parametrize_plus(f, host_class_or_module):
            return _decorate(f, host_class_or_module)
        return _apply_parametrize_plus
    else:
        return _decorate


class InvalidIdTemplateException(Exception):
    """
    Raised when a string template provided in an `idgen` raises an error
    """
    def __init__(self, idgen, params, caught):
        self.idgen = idgen
        self.params = params
        self.caught = caught
        super(InvalidIdTemplateException, self).__init__()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Error generating test id using name template '%s' with parameter values " \
               "%r. Please check the name template. Caught: %s - %s" \
               % (self.idgen, self.params, self.caught.__class__, self.caught)


def _parametrize_plus(argnames=None,   # type: Union[str, Tuple[str], List[str]]
                      argvalues=None,  # type: Iterable[Any]
                      indirect=False,  # type: bool
                      ids=None,        # type: Union[Callable, Iterable[str]]
                      idstyle=None,    # type: Optional[Union[str, Callable]]
                      idgen=_IDGEN,    # type: Union[str, Callable]
                      auto_refs=True,  # type: bool
                      scope=None,      # type: str
                      hook=None,       # type: Callable[[Callable], Callable]
                      debug=False,     # type: bool
                      **args):
    # type: (...) -> Tuple[Callable[[T], T], bool]
    """

    :return: a tuple (decorator, needs_inject) where needs_inject is True if decorator has signature (f, host)
        and False if decorator has signature (f)
    """
    # first handle argnames / argvalues (new modes of input)
    argnames, argvalues = _get_argnames_argvalues(argnames, argvalues, **args)

    # argnames related
    initial_argnames = ','.join(argnames)
    nb_params = len(argnames)

    # extract all marks and custom ids.
    # Do not check consistency of sizes argname/argvalue as a fixture_ref can stand for several argvalues.
    marked_argvalues = argvalues
    has_cust_ids = (idgen is not _IDGEN or len(args) > 0) or (ids is not None)
    p_ids, p_marks, argvalues, fixture_indices, mod_lvid_indices = \
        _process_argvalues(argnames, marked_argvalues, nb_params, has_cust_ids, auto_refs=auto_refs)

    # idgen default
    if idgen is _IDGEN:
        # default: use the new id style only when some keyword **args are provided and there are no fixture refs
        idgen = AUTO if (len(args) > 0 and len(fixture_indices) == 0 and ids is None) else None

    if idgen is AUTO:
        # note: we use a "trick" here with mini_idval to get the appropriate result (argname='', idx=v)
        def _make_ids(**args):
            for n, v in args.items():
                yield "%s=%s" % (n, mini_idval(val=v, argname='', idx=v))

        idgen = lambda **args: "-".join(_make_ids(**args))  # noqa

    # generate id
    if idgen is not None:
        if ids is not None:
            raise ValueError("Only one of `ids` and `idgen` should be provided")
        ids = _gen_ids(argnames, argvalues, idgen)

    if len(fixture_indices) == 0:
        # No fixture refernce: fallback to a standard pytest.mark.parametrize
        if debug:
            print("No fixture reference found. Calling @pytest.mark.parametrize...")
            print(" - argnames: %s" % initial_argnames)
            print(" - argvalues: %s" % marked_argvalues)
            print(" - ids: %s" % ids)

        # handle infinite iterables like latest pytest, for convenience
        ids = resolve_ids(ids, marked_argvalues, full_resolve=False)

        # no fixture reference: shortcut, do as usual (note that the hook wont be called since no fixture is created)
        _decorator = pytest.mark.parametrize(initial_argnames, marked_argvalues, indirect=indirect,
                                             ids=ids, scope=scope)
        if indirect:
            return _decorator, False
        else:
            # wrap the decorator to check if the test function has the parameters as arguments
            def _apply(test_func):
                # type: (...) -> Callable[[T], T]
                if not safe_isclass(test_func):
                    # a Function: raise a proper error message if improper use
                    s = signature(test_func)
                    for p in argnames:
                        if p not in s.parameters:
                            raise ValueError("parameter '%s' not found in test function signature '%s%s'"
                                             "" % (p, test_func.__name__, s))
                else:
                    # a Class: we cannot really perform any check.
                    pass
                return _decorator(test_func)

        return _apply, False

    else:
        # there are fixture references: we will create a specific decorator replacing the params with a "union" fixture
        if indirect:
            warn("Using `indirect=True` at the same time as fixture references in `@parametrize` is not guaranteed to "
                 "work and is strongly discouraged for readability reasons. See "
                 "https://github.com/smarie/python-pytest-cases/issues/150")

        # First unset the pytest.param id we have set earlier in _process_argvalues: indeed it is only needed in
        # the case above where we were defaulting to legacy @pytest.mark.parametrize .
        # Here we have fixture refs so we will create a fixture union with several ParamAlternative, and their id will
        # anyway be generated with `mini_idvalset` which tackles the case of lazy_value used for a tuple of args
        for i in mod_lvid_indices:
            p_ids[i] = None
            if p_marks[i]:
                marked_argvalues[i] = ParameterSet(values=marked_argvalues[i].values, id=None, marks=p_marks[i])
            else:
                marked_argvalues[i] = argvalues[i]  # we can even remove the pytest.param wrapper

        if indirect:
            raise ValueError("Setting `indirect=True` is not yet supported when at least a `fixure_ref` is present in "
                             "the `argvalues`.")

        if debug:
            print("Fixture references found. Creating references and fixtures...")

        param_names_str = '_'.join(argnames).replace(' ', '')

        # Are there explicit ids provided ?
        explicit_ids_to_use = False
        ids = resolve_ids(ids, argvalues, full_resolve=False)
        if isinstance(ids, list):
            explicit_ids_to_use = True

        # First define a few functions that will help us create the various fixtures to use in the final "union"

        def _create_params_alt(fh, test_func, union_name, from_i, to_i, hook):  # noqa
            """ Routine that will be used to create a parameter fixture for argvalues between prev_i and i"""

            # is this about a single value or several values ?
            if to_i == from_i + 1:
                i = from_i
                del from_i

                # If an explicit list of ids was provided, slice it. Otherwise use the provided callable
                if ids is not None:
                    _id = ids[i] if explicit_ids_to_use else ids(argvalues[i])
                else:
                    _id = None

                return SingleParamAlternative.create(new_fixture_host=fh, test_func=test_func,
                                                     param_union_name=union_name, argnames=argnames, i=i,
                                                     argvalue=marked_argvalues[i], id=_id,
                                                     hook=hook, debug=debug)
            else:
                # If an explicit list of ids was provided, slice it. Otherwise the provided callable will be used later
                _ids = ids[from_i:to_i] if explicit_ids_to_use else ids

                return MultiParamAlternative.create(new_fixture_host=fh, test_func=test_func,
                                                    param_union_name=union_name, argnames=argnames, from_i=from_i,
                                                    to_i=to_i, argvalues=marked_argvalues[from_i:to_i], ids=_ids,
                                                    hook=hook, debug=debug)


        def _create_fixture_ref_alt(union_name, test_func, i):  # noqa

            # If an explicit list of ids was provided, slice it. Otherwise use the provided callable
            if ids is not None:
                _id = ids[i] if explicit_ids_to_use else ids(argvalues[i])
            else:
                _id = None

            # Get the referenced fixture name
            f_fix_name = argvalues[i].fixture

            if debug:
                print(" - Creating reference to existing fixture %r" % (f_fix_name,))

            # Create the alternative
            f_fix_alt = FixtureParamAlternative(union_name=union_name, fixture_ref=argvalues[i],
                                                decorated=test_func, argnames=argnames, param_index=i, id=_id)
            # Finally copy the custom id/marks on the FixtureParamAlternative if any
            if is_marked_parameter_value(marked_argvalues[i]):
                f_fix_alt = ParameterSet(values=(f_fix_alt,),
                                         id=get_marked_parameter_id(marked_argvalues[i]),
                                         marks=get_marked_parameter_marks(marked_argvalues[i]))

            return f_fix_alt

        def _create_fixture_ref_product(fh, union_name, i, fixture_ref_positions, test_func, hook):  # noqa

            # If an explicit list of ids was provided, slice it. Otherwise the provided callable will be used
            _id = ids[i] if explicit_ids_to_use else ids

            # values to use:
            param_values = argvalues[i]

            # Create a unique fixture name
            p_fix_name = "%s_%s_P%s" % (test_func.__name__, param_names_str, i)
            p_fix_name = check_name_available(fh, p_fix_name, if_name_exists=CHANGE, caller=parametrize)

            if debug:
                print(" - Creating new fixture %r to handle parameter %s that is a cross-product" % (p_fix_name, i))

            # Create the fixture
            _make_fixture_product(fh, name=p_fix_name, hook=hook, caller=parametrize,
                                  fixtures_or_values=param_values, fixture_positions=fixture_ref_positions)

            # Create the corresponding alternative
            p_fix_alt = ProductParamAlternative(union_name=union_name, alternative_name=p_fix_name, decorated=test_func,
                                                argval=argvalues[i], argnames=argnames, param_index=i, id=_id)
            # copy the custom id/marks to the ParamAlternative if any
            if is_marked_parameter_value(marked_argvalues[i]):
                p_fix_alt = ParameterSet(values=(p_fix_alt,),
                                         id=get_marked_parameter_id(marked_argvalues[i]),
                                         marks=get_marked_parameter_marks(marked_argvalues[i]))
            return p_fix_alt

        # Then create the decorator per se
        def parametrize_plus_decorate(test_func, fixtures_dest):
            # type: (...) -> Callable[[T], T]
            """
            A decorator that wraps the test function so that instead of receiving the parameter names, it receives the
            new fixture. All other decorations are unchanged.

            :param test_func:
            :return:
            """
            test_func_name = test_func.__name__

            # first check if the test function has the parameters as arguments
            if safe_isclass(test_func):
                # a test class: not supported yet
                raise NotImplementedError("@parametrize can not be used to decorate a Test class when the argvalues "
                                          "contain at least one reference to a fixture.")

            old_sig = signature(test_func)
            for p in argnames:
                if p not in old_sig.parameters:
                    raise ValueError("parameter '%s' not found in test function signature '%s%s'"
                                     "" % (p, test_func_name, old_sig))

            # The name for the final "union" fixture
            # style_template = "%s_param__%s"
            main_fixture_style_template = "%s_%s"
            fixture_union_name = main_fixture_style_template % (test_func_name, param_names_str)
            fixture_union_name = check_name_available(fixtures_dest, fixture_union_name, if_name_exists=CHANGE,
                                                      caller=parametrize)

            # Retrieve (if ref) or create (for normal argvalues) the fixtures that we will union
            fixture_alternatives = []
            prev_i = -1
            for i, j_list in fixture_indices:  # noqa
                # A/ Is there any non-empty group of 'normal' parameters before the fixture_ref at <i> ? If so, handle.
                if i > prev_i + 1:
                    # create a new "param" fixture parametrized with all of that consecutive group.
                    # Important note: we could either wish to create one fixture for parameter value or to create
                    #  one for each consecutive group as shown below. This should not lead to different results but perf
                    #  might differ. Maybe add a parameter in the signature so that users can test it ?
                    #  this would make the ids more readable by removing the "P2toP3"-like ids
                    p_fix_alt = _create_params_alt(fixtures_dest, test_func=test_func, hook=hook,
                                                   union_name=fixture_union_name, from_i=prev_i + 1, to_i=i)
                    fixture_alternatives.append(p_fix_alt)

                # B/ Now handle the fixture ref at position <i>
                if j_list is None:
                    # argvalues[i] contains a single argvalue that is a fixture_ref : add the referenced fixture
                    f_fix_alt = _create_fixture_ref_alt(union_name=fixture_union_name, test_func=test_func, i=i)
                    fixture_alternatives.append(f_fix_alt)
                else:
                    # argvalues[i] is a tuple, some of them being fixture_ref. create a fixture refering to all of them
                    prod_fix_alt = _create_fixture_ref_product(fixtures_dest, union_name=fixture_union_name, i=i,
                                                               fixture_ref_positions=j_list,
                                                               test_func=test_func, hook=hook)
                    fixture_alternatives.append(prod_fix_alt)

                prev_i = i

            # C/ handle last consecutive group of normal parameters, if any
            i = len(argvalues)  # noqa
            if i > prev_i + 1:
                p_fix_alt = _create_params_alt(fixtures_dest, test_func=test_func, hook=hook,
                                               union_name=fixture_union_name, from_i=prev_i + 1, to_i=i)
                fixture_alternatives.append(p_fix_alt)

            # if fixtures_to_union has length 1, simplify ? >> No, we leave such "optimization" to the end user

            # Handle the list of alternative names. Duplicates should be removed here
            fix_alt_names = []
            for alt in fixture_alternatives:
                if is_marked_parameter_value(alt):
                    # wrapped by a pytest.param
                    alt = get_marked_parameter_values(alt, nbargs=1)
                    assert len(alt) == 1, "Error with alternative please report"
                    alt = alt[0]
                if alt.alternative_name not in fix_alt_names:
                    fix_alt_names.append(alt.alternative_name)
                else:
                    # non-unique alt fixture names should only happen when the alternative is a fixture reference
                    assert isinstance(alt, FixtureParamAlternative), "Created fixture names not unique, please report"

            # Finally create a "main" fixture with a unique name for this test function
            if debug:
                print("Creating final union fixture %r with alternatives %r"
                      % (fixture_union_name, UnionFixtureAlternative.to_list_of_fixture_names(fixture_alternatives)))

            # use the custom subclass of idstyle that was created for ParamAlternatives
            if idstyle is None or isinstance(idstyle, string_types):
                _idstyle = ParamIdMakers.get(idstyle)
            else:
                _idstyle = idstyle

            # note: the function automatically registers it in the module
            _make_fixture_union(fixtures_dest, name=fixture_union_name, hook=hook, caller=parametrize,
                                fix_alternatives=fixture_alternatives, unique_fix_alt_names=fix_alt_names,
                                idstyle=_idstyle, scope=scope)

            # --create the new test function's signature that we want to expose to pytest
            # it is the same than existing, except that we want to replace all parameters with the new fixture
            # first check where we should insert the new parameters (where is the first param we remove)
            _first_idx = -1
            for _first_idx, _n in enumerate(old_sig.parameters):
                if _n in argnames:
                    break
            # then remove all parameters that will be replaced by the new fixture
            new_sig = remove_signature_parameters(old_sig, *argnames)
            # finally insert the new fixture in that position. Indeed we can not insert first or last, because
            # 'self' arg (case of test class methods) should stay first and exec order should be preserved when possible
            new_sig = add_signature_parameters(new_sig, custom_idx=_first_idx,
                                               custom=Parameter(fixture_union_name,
                                                                kind=Parameter.POSITIONAL_OR_KEYWORD))

            if debug:
                print("Creating final test function wrapper with signature %s%s" % (test_func_name, new_sig))

            # --Finally create the fixture function, a wrapper of user-provided fixture with the new signature
            def replace_paramfixture_with_values(kwargs):  # noqa
                # remove the created fixture value
                encompassing_fixture = kwargs.pop(fixture_union_name)
                # and add instead the parameter values
                if nb_params > 1:
                    for i, p in enumerate(argnames):  # noqa
                        try:
                            kwargs[p] = encompassing_fixture[i]
                        except TypeError:
                            raise Exception("Unable to unpack parameter value to a tuple: %r" % encompassing_fixture)
                else:
                    kwargs[argnames[0]] = encompassing_fixture
                # return
                return kwargs

            if not isgeneratorfunction(test_func):
                # normal test or fixture function with return statement
                @wraps(test_func, new_sig=new_sig)
                def wrapped_test_func(*args, **kwargs):  # noqa
                    if kwargs.get(fixture_union_name, None) is NOT_USED:
                        # TODO why this ? it is probably useless: this fixture
                        #  is private and will never end up in another union
                        return NOT_USED
                    else:
                        replace_paramfixture_with_values(kwargs)
                        return test_func(*args, **kwargs)

            else:
                # generator test or fixture function (with one or several yield statements)
                @wraps(test_func, new_sig=new_sig)
                def wrapped_test_func(*args, **kwargs):  # noqa
                    if kwargs.get(fixture_union_name, None) is NOT_USED:
                        # TODO why this ? it is probably useless: this fixture
                        #  is private and will never end up in another union
                        yield NOT_USED
                    else:
                        replace_paramfixture_with_values(kwargs)
                        for res in test_func(*args, **kwargs):
                            yield res

            # move all pytest marks from the test function to the wrapper
            # not needed because the __dict__ is automatically copied when we use @wraps
            #   move_all_pytest_marks(test_func, wrapped_test_func)

            # With this hack we will be ordered correctly by pytest https://github.com/pytest-dev/pytest/issues/4429
            try:
                # propagate existing attribute if any
                wrapped_test_func.place_as = test_func.place_as
            except:  # noqa
                # position the test at the original function's position
                wrapped_test_func.place_as = test_func

            # return the new test function
            return wrapped_test_func

        return parametrize_plus_decorate, True


def _get_argnames_argvalues(
    argnames=None,   # type: Union[str, Tuple[str], List[str]]
    argvalues=None,  # type: Iterable[Any]
    **args
):
    """

    :param argnames:
    :param argvalues:
    :param args:
    :return: argnames, argvalues - both guaranteed to be lists
    """
    # handle **args - a dict of {argnames: argvalues}
    if len(args) > 0:
        kw_argnames, kw_argvalues = cart_product_pytest(tuple(args.keys()), tuple(args.values()))
    else:
        kw_argnames, kw_argvalues = (), ()

    if argnames is None:
        # (1) all {argnames: argvalues} pairs are provided in **args
        if argvalues is not None or len(args) == 0:
            raise ValueError("No parameters provided")

        argnames = kw_argnames
        argvalues = kw_argvalues
        # simplify if needed to comply with pytest.mark.parametrize
        if len(argnames) == 1:
            argvalues = [_l[0] if not is_marked_parameter_value(_l) else _l for _l in argvalues]
        return argnames, argvalues

    if isinstance(argnames, string_types):
        # (2) argnames + argvalues, as usual. However **args can also be passed and should be added
        argnames = get_param_argnames_as_list(argnames)

    if not isinstance(argnames, (list, tuple)):
        raise TypeError("argnames should be a string, list or a tuple")

    if any([not isinstance(argname, str) for argname in argnames]):
        raise TypeError("all argnames should be strings")

    if argvalues is None:
        raise ValueError("No argvalues provided while argnames are provided")

    # transform argvalues to a list (it can be a generator)
    try:
        argvalues = list(argvalues)
    except TypeError:
        raise InvalidParamsList(argvalues)

    # append **args
    if len(kw_argnames) > 0:
        argnames, argvalues = cart_product_pytest((argnames, kw_argnames),
                                                  (argvalues, kw_argvalues))

    return argnames, argvalues


def _gen_ids(argnames, argvalues, idgen):
    """
    Generates an explicit test ids list from a non-none `idgen`.

    `idgen` should be either a callable of a string template.

    :param argnames:
    :param argvalues:
    :param idgen:
    :return:
    """
    if not callable(idgen):
        # idgen is a new-style string formatting template
        if not isinstance(idgen, string_types):
            raise TypeError("idgen should be a callable or a string, found: %r" % idgen)

        _formatter = idgen

        def gen_id_using_str_formatter(**params):
            try:
                # format using the idgen template
                return _formatter.format(**params)
            except Exception as e:
                raise InvalidIdTemplateException(_formatter, params, e)

        idgen = gen_id_using_str_formatter

    if len(argnames) > 1:
        ids = [idgen(**{n: v for n, v in zip(argnames, _argvals)}) for _argvals in argvalues]
    else:
        _only_name = argnames[0]
        ids = [idgen(**{_only_name: v}) for v in argvalues]

    return ids


def _process_argvalues(argnames, marked_argvalues, nb_params, has_custom_ids, auto_refs):
    """Internal method to use in _pytest_parametrize_plus

    Processes the provided marked_argvalues (possibly marked with pytest.param) and returns
    p_ids, p_marks, argvalues (not marked with pytest.param), fixture_indices

    Note: `marked_argvalues` is modified in the process if a `lazy_value` is found with a custom id or marks.

    :param argnames:
    :param marked_argvalues:
    :param nb_params:
    :param has_custom_ids: a boolean indicating if custom ids are provided separately in `ids` or `idgen` (see
        @parametrize)
    :param auto_refs: if True, a `fixture_ref` will be created around fixture symbols used as argvalues automatically
    :return:
    """
    p_ids, p_marks, argvalues = extract_parameterset_info(argnames, marked_argvalues, check_nb=False)

    # find if there are fixture references or lazy values in the values provided
    fixture_indices = []
    mod_lvid_indices = []  # indices of lazy_values for which we created a wrapper pytest.param with an id
    if nb_params == 1:
        for i, v in enumerate(argvalues):
            if is_lazy_value(v):
                # --- A lazy value is used for several parameters at the same time ---
                # Users can declare custom marks in the lazy value API, we have to take these into account
                # (1) if there was a pytest.param around it, we have to merge the marks from the lazy value into it
                # (2) if there was no pytest.param around it and there are marks, we have to create the pytest.param
                # Note: a custom id in lazy value does not require such processing as it does not need to take
                # precedence over `ids` or `idgen`

                # are there any marks ? (either added with lazy_value(marks=), or on the function itself)
                _mks = v.get_marks(as_decorators=True)
                if len(_mks) > 0:
                    # update/create the pytest.param marks on this value
                    p_marks[i] = (p_marks[i] + _mks) if p_marks[i] is not None else _mks

                    # update the original marked_argvalues. Note that argvalues[i] = v
                    marked_argvalues[i] = ParameterSet(values=(argvalues[i],), id=p_ids[i], marks=p_marks[i])
            else:
                if auto_refs and is_fixture(v):
                    # auto create wrapper fixture_refs
                    argvalues[i] = v = fixture_ref(v)
                    if p_ids[i] is None and p_marks[i] is None:
                        marked_argvalues[i] = v
                    else:
                        marked_argvalues[i] = ParameterSet(values=(v,), id=p_ids[i], marks=p_marks[i])

                if isinstance(v, fixture_ref):
                    # Fix the referenced fixture length
                    v.theoretical_size = nb_params
                    fixture_indices.append((i, None))

    elif nb_params > 1:
        for i, v in enumerate(argvalues):

            # A/ First analyze what is the case at hand
            _lazyvalue_used_as_tuple = False
            _fixtureref_used_as_tuple = False
            if is_lazy_value(v):
                _lazyvalue_used_as_tuple = True
            else:
                if auto_refs and is_fixture(v):
                    # auto create wrapper fixture_refs
                    argvalues[i] = v = fixture_ref(v)
                    if p_ids[i] is None and p_marks[i] is None:
                        marked_argvalues[i] = v
                    else:
                        marked_argvalues[i] = ParameterSet(values=(v,), id=p_ids[i], marks=p_marks[i])

                if isinstance(v, fixture_ref):
                    # Fix the referenced fixture length
                    v.theoretical_size = nb_params
                    _fixtureref_used_as_tuple = True
                elif len(v) == 1:
                    # same than above but it was in a pytest.param
                    if is_lazy_value(v[0]):
                        argvalues[i] = v = v[0]
                        _lazyvalue_used_as_tuple = True
                    else:
                        if auto_refs and is_fixture(v[0]):
                            # auto create wrapper fixture_refs
                            v = (fixture_ref(v[0]),)

                        if isinstance(v[0], fixture_ref):
                            _fixtureref_used_as_tuple = True
                            argvalues[i] = v = v[0]
                            if p_ids[i] is None and p_marks[i] is None:
                                marked_argvalues[i] = v
                            else:
                                marked_argvalues[i] = ParameterSet(values=(v,), id=p_ids[i], marks=p_marks[i])
                            # Fix the referenced fixture length
                            v.theoretical_size = nb_params

            # B/ Now process it
            if _lazyvalue_used_as_tuple:
                # --- A lazy value is used for several parameters at the same time ---

                # Since users have the possibility in the lazy value API to declare a custom id or custom marks,
                # we have to take these into account.
                # MARKS:
                # (1) if there was a pytest.param around it, we have to merge the marks from the lazy value into it
                # (2) if there was no pytest.param around it and there are marks, we have to create the pytest.param
                # IDS:
                # As opposed to the case of nb_params=1, we can not let pytest generate the id as it would create a
                # tuple of LazyTupleItem ids (e.g. <id>[0]-<id>[1]-...). So
                # (1) if there is a custom id list or generator, do not care about this.
                # (2) if there is a pytest.param with a custom id, do not care about this
                # (3) if there is nothing OR if there is a pytest.param with no id, we should create a pytest.param with
                # the id.

                # in this particular case we have to modify the initial list
                argvalues[i] = v.as_lazy_tuple(nb_params)

                # TUPLE usage: if the id is not provided elsewhere we HAVE to set an id to avoid <id>[0]-<id>[1]...
                if p_ids[i] is None and not has_custom_ids:
                    if not has_pytest_param:
                        if v._id is not None:
                            # (on pytest 2 we cannot do it since pytest.param does not exist)
                            warn("The custom id %r in `lazy_value` will be ignored as this version of pytest is too old"
                                 " to support `pytest.param`." % v._id)
                        else:
                            pass  # no warning, but no p_id update
                    else:
                        # update/create the pytest.param id on this value
                        p_ids[i] = v.get_id()
                        mod_lvid_indices.append(i)

                # handle marks
                _mks = v.get_marks(as_decorators=True)
                if len(_mks) > 0:
                    # update/create the pytest.param marks on this value
                    p_marks[i] = (p_marks[i] + _mks) if p_marks[i] is not None else _mks

                # update the marked_argvalues
                # - at least with the unpacked lazytuple if no pytest.param is there or needs to be created
                # - with a pytest.param if one is needed
                if p_ids[i] is None and p_marks[i] is None:
                    marked_argvalues[i] = argvalues[i]
                else:
                    # note that here argvalues[i] IS a tuple-like so we do not create a tuple around it
                    marked_argvalues[i] = ParameterSet(values=argvalues[i], id=p_ids[i], marks=p_marks[i] or ())

            elif _fixtureref_used_as_tuple:
                # a fixture ref is used for several parameters at the same time
                fixture_indices.append((i, None))
            else:
                # Tuple: check nb params for consistency
                if len(v) != len(argnames):
                    raise ValueError("Inconsistent number of values in pytest parametrize: %s items found while the "
                                     "number of parameters is %s: %s." % (len(v), len(argnames), v))

                # let's dig into the tuple to check if there are fixture_refs or lazy_values
                lv_pos_list = [j for j, _pval in enumerate(v) if is_lazy_value(_pval)]
                if len(lv_pos_list) > 0:
                    _mks = [mk for _lv in lv_pos_list for mk in v[_lv].get_marks(as_decorators=True)]
                    if len(_mks) > 0:
                        # update/create the pytest.param marks on this value (global). (id not taken into account)
                        p_marks[i] = (list(p_marks[i]) + _mks) if p_marks[i] is not None else list(_mks)
                        marked_argvalues[i] = ParameterSet(values=argvalues[i], id=p_ids[i], marks=p_marks[i] or ())

                # auto create fixtures
                if auto_refs:
                    autofix_pos_list = [j for j, _pval in enumerate(v) if is_fixture(_pval)]
                    if len(autofix_pos_list) > 0:
                        # there is at least one fixture without wrapping ref inside the tuple
                        autov = list(v)
                        for _k in autofix_pos_list:
                            autov[_k] = fixture_ref(autov[_k])
                        argvalues[i] = v = tuple(autov)
                        if p_ids[i] is None and p_marks[i] is None:
                            marked_argvalues[i] = argvalues[i]
                        else:
                            # note that here argvalues[i] IS a tuple-like so we do not create a tuple around it
                            marked_argvalues[i] = ParameterSet(values=argvalues[i], id=p_ids[i], marks=p_marks[i] or ())

                fix_pos_list = [j for j, _pval in enumerate(v) if isinstance(_pval, fixture_ref)]
                if len(fix_pos_list) > 0:
                    # there is at least one fixture ref inside the tuple
                    fixture_indices.append((i, fix_pos_list))

                # let's dig into the tuple
                # has_val_ref = any(isinstance(_pval, lazy_value) for _pval in v)
                # val_pos_list = [j for j, _pval in enumerate(v) if isinstance(_pval, lazy_value)]
                # if len(val_pos_list) > 0:
                #     # there is at least one value ref inside the tuple
                #     argvalues[i] = tuple_with_value_refs(v, theoreticalsize=nb_params, positions=val_pos_list)

    return p_ids, p_marks, argvalues, fixture_indices, mod_lvid_indices
