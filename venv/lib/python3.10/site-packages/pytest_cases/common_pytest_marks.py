# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
import itertools

import warnings
from distutils.version import LooseVersion

try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature  # noqa

try:
    from typing import Iterable, Optional, Tuple, List, Set, Union, Sequence  # noqa
except ImportError:
    pass

import pytest

try:
    from _pytest.mark.structures import MarkDecorator, Mark  # noqa
except ImportError:
    from _pytest.mark import MarkDecorator, MarkInfo as Mark  # noqa

from .common_mini_six import string_types


PYTEST_VERSION = LooseVersion(pytest.__version__)
PYTEST3_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.0.0')
PYTEST32_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.2.0')
PYTEST33_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.3.0')
PYTEST34_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.4.0')
PYTEST35_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.5.0')
PYTEST361_36X = LooseVersion('3.6.0') < PYTEST_VERSION < LooseVersion('3.7.0')
PYTEST37_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.7.0')
PYTEST38_OR_GREATER = PYTEST_VERSION >= LooseVersion('3.8.0')
PYTEST46_OR_GREATER = PYTEST_VERSION >= LooseVersion('4.6.0')
PYTEST53_OR_GREATER = PYTEST_VERSION >= LooseVersion('5.3.0')
PYTEST54_OR_GREATER = PYTEST_VERSION >= LooseVersion('5.4.0')
PYTEST421_OR_GREATER = PYTEST_VERSION >= LooseVersion('4.2.1')
PYTEST6_OR_GREATER = PYTEST_VERSION >= LooseVersion('6.0.0')
PYTEST7_OR_GREATER = PYTEST_VERSION >= LooseVersion('7.0.0')
PYTEST71_OR_GREATER = PYTEST_VERSION >= LooseVersion('7.1.0')


def get_param_argnames_as_list(argnames):
    """
    pytest parametrize accepts both coma-separated names and list/tuples.
    This function makes sure that we always return a list
    :param argnames:
    :return:
    """
    if isinstance(argnames, string_types):
        argnames = argnames.replace(' ', '').split(',')
    return list(argnames)


# noinspection PyUnusedLocal
def _pytest_mark_parametrize(argnames, argvalues, ids=None, indirect=False, scope=None, **kwargs):
    """ Fake method to have a reference signature of pytest.mark.parametrize"""
    pass


def get_parametrize_signature():
    """

    :return: a reference signature representing
    """
    return signature(_pytest_mark_parametrize)


class _ParametrizationMark:
    """
    Container for the mark information that we grab from the fixtures (`@fixture`)

    Represents the information required by `@fixture` to work.
    """
    __slots__ = "param_names", "param_values", "param_ids"

    def __init__(self, mark):
        bound = get_parametrize_signature().bind(*mark.args, **mark.kwargs)
        try:
            remaining_kwargs = bound.arguments['kwargs']
        except KeyError:
            pass
        else:
            if len(remaining_kwargs) > 0:
                warnings.warn("parametrize kwargs not taken into account: %s. Please report it at"
                              " https://github.com/smarie/python-pytest-cases/issues" % remaining_kwargs)
        self.param_names = get_param_argnames_as_list(bound.arguments['argnames'])
        self.param_values = bound.arguments['argvalues']
        try:
            bound.apply_defaults()
            self.param_ids = bound.arguments['ids']
        except AttributeError:
            # can happen if signature is from funcsigs so we have to apply ourselves
            self.param_ids = bound.arguments.get('ids', None)


# -------- tools to get the parametrization mark whatever the pytest version
class _LegacyMark:
    __slots__ = "args", "kwargs"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


# ---------------- working on functions
def copy_pytest_marks(from_f, to_f, override=False):
    """Copy all pytest marks from a function or class to another"""
    from_marks = get_pytest_marks_on_function(from_f)
    to_marks = [] if override else get_pytest_marks_on_function(to_f)
    # note: the new marks are appended *after* existing if no override
    to_f.pytestmark = to_marks + from_marks


def filter_marks(marks,  # type: Iterable[Mark]
                 remove  # type: str
                 ):
    # type: (...) -> Tuple[Mark]
    """
    Returns a tuple of all marks in `marks` that do not have a 'parametrize' name.

    :param marks:
    :param remove:
    :return:
    """
    return tuple(m for m in marks if m.name != remove)


def get_pytest_marks_on_function(f,
                                 as_decorators=False  # type: bool
                                 ):
    # type: (...) -> Union[List[Mark], List[MarkDecorator]]
    """
    Utility to return a list of *ALL* pytest marks (not only parametrization) applied on a function
    Note that this also works on classes

    :param f:
    :param as_decorators: transforms the marks into decorators before returning them
    :return:
    """
    try:
        mks = f.pytestmark
    except AttributeError:
        try:
            # old pytest < 3: marks are set as fields on the function object
            # but they do not have a particular type, their type is 'instance'...
            mks = [v for v in vars(f).values() if str(v).startswith("<MarkInfo '")]
        except AttributeError:
            return []

    # in the new version of pytest the marks have to be transformed into decorators explicitly
    if as_decorators:
        return markinfos_to_markdecorators(mks, function_marks=True)
    else:
        return mks


def get_pytest_marks_on_item(item):
    """lists all marks on an item such as `request._pyfuncitem`"""
    if PYTEST3_OR_GREATER:
        return item.callspec.marks
    else:
        return [val for val in item.keywords.values() if isinstance(val, (MarkDecorator, Mark))]


def get_pytest_usefixture_marks(f):
    # pytest > 3.2.0
    marks = getattr(f, 'pytestmark', None)
    if marks is not None:
        return tuple(itertools.chain.from_iterable(
            mark.args for mark in marks if mark.name == 'usefixtures'
        ))
    else:
        # older versions
        mark_info = getattr(f, 'usefixtures', None)
        if mark_info is not None:
            return mark_info.args
        else:
            return ()


def remove_pytest_mark(f, mark_name):
    marks = getattr(f, 'pytestmark', None)
    if marks is not None:
        # pytest > 3.2.0
        new_marks = [m for m in marks if m.name != mark_name]
        f.pytestmark = new_marks
    else:
        # older versions
        try:
            delattr(f, mark_name)
        except AttributeError:
            pass
    return f


def get_pytest_parametrize_marks(f):
    """
    Returns the @pytest.mark.parametrize marks associated with a function (and only those)

    :param f:
    :return: a tuple containing all 'parametrize' marks
    """
    # pytest > 3.2.0
    marks = getattr(f, 'pytestmark', None)
    if marks is not None:
        return tuple(_ParametrizationMark(m) for m in marks if m.name == 'parametrize')
    else:
        # older versions
        mark_info = getattr(f, 'parametrize', None)
        if mark_info is not None:
            # mark_info.args contains a list of (name, values)
            if len(mark_info.args) % 2 != 0:
                raise ValueError("internal pytest compatibility error - please report")
            nb_parametrize_decorations = len(mark_info.args) // 2
            if nb_parametrize_decorations > 1 and len(mark_info.kwargs) > 0:
                raise ValueError("Unfortunately with this old pytest version it is not possible to have several "
                                 "parametrization decorators while specifying **kwargs, as all **kwargs are "
                                 "merged, leading to inconsistent results. Either upgrade pytest, remove the **kwargs,"
                                 "or merge all the @parametrize decorators into a single one. **kwargs: %s"
                                 % mark_info.kwargs)
            res = []
            for i in range(nb_parametrize_decorations):
                param_name, param_values = mark_info.args[2*i:2*(i+1)]
                res.append(_ParametrizationMark(_LegacyMark(param_name, param_values, **mark_info.kwargs)))
            return tuple(res)
        else:
            return ()


# ---- tools to reapply marks on test parameter values, whatever the pytest version ----

# Compatibility for the way we put marks on single parameters in the list passed to @pytest.mark.parametrize
# see https://docs.pytest.org/en/3.3.0/skipping.html?highlight=mark%20parametrize#skip-xfail-with-parametrize

# check if pytest.param exists
has_pytest_param = hasattr(pytest, 'param')


if not has_pytest_param:
    # if not this is how it was done
    # see e.g. https://docs.pytest.org/en/2.9.2/skipping.html?highlight=mark%20parameter#skip-xfail-with-parametrize
    def make_marked_parameter_value(argvalues_tuple, marks):
        if len(marks) > 1:
            raise ValueError("Multiple marks on parameters not supported for old versions of pytest")
        else:
            if not isinstance(argvalues_tuple, tuple):
                raise TypeError("argvalues must be a tuple !")

            # get a decorator for each of the markinfo
            marks_mod = markinfos_to_markdecorators(marks, function_marks=False)

            # decorate. We need to distinguish between single value and multiple values
            # indeed in pytest 2 a single arg passed to the decorator is passed directly
            # (for example: @pytest.mark.skip(1) in parametrize)
            return marks_mod[0](argvalues_tuple) if len(argvalues_tuple) > 1 else marks_mod[0](argvalues_tuple[0])
else:
    # Otherwise pytest.param exists, it is easier
    def make_marked_parameter_value(argvalues_tuple, marks):
        if not isinstance(argvalues_tuple, tuple):
            raise TypeError("argvalues must be a tuple !")

        # get a decorator for each of the markinfo
        marks_mod = markinfos_to_markdecorators(marks, function_marks=False)

        # decorate
        return pytest.param(*argvalues_tuple, marks=marks_mod)


def markinfos_to_markdecorators(marks,                # type: Iterable[Mark]
                                function_marks=False  # type: bool
                                ):
    # type: (...) -> List[MarkDecorator]
    """
    Transforms the provided marks (MarkInfo or Mark in recent pytest) obtained from marked cases, into MarkDecorator so
    that they can be re-applied to generated pytest parameters in the global @pytest.mark.parametrize.

    Returns a list.

    :param marks:
    :param function_marks:
    :return:
    """
    marks_mod = []
    try:
        # suppress the warning message that pytest generates when calling pytest.mark.MarkDecorator() directly
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for m in marks:
                # create a dummy new MarkDecorator named "MarkDecorator" for reference
                md = pytest.mark.MarkDecorator()

                if PYTEST3_OR_GREATER:
                    if isinstance(m, type(md)):
                        # already a decorator, we can use it
                        marks_mod.append(m)
                    else:
                        md.mark = m
                        marks_mod.append(md)
                else:
                    # always recreate one, type comparison does not work (all generic stuff)
                    md.name = m.name
                    # md.markname = m.name
                    if function_marks:
                        md.args = m.args  # a mark on a function does not include the function in the args
                    else:
                        md.args = m.args[:-1]  # not a function: the value is in the args, remove it
                    md.kwargs = m.kwargs

                    # markinfodecorator = getattr(pytest.mark, markinfo.name)
                    # markinfodecorator(*markinfo.args)

                    marks_mod.append(md)

    except Exception as e:
        warnings.warn("Caught exception while trying to mark case: [%s] %s" % (type(e), e))
    return marks_mod


def markdecorators_as_tuple(marks  # type: Optional[Union[MarkDecorator, Iterable[MarkDecorator]]]
                            ):
    # type: (...) -> Tuple[MarkDecorator, ...]
    """
    Internal routine used to normalize marks received from users in a `marks=` parameter

    :param marks:
    :return:
    """
    if marks is None:
        return ()

    try:
        # iterable ?
        return tuple(marks)
    except TypeError:
        # single
        return (marks,)


def markdecorators_to_markinfos(marks  # type: Sequence[MarkDecorator]
                                ):
    # type: (...) -> Tuple[Mark, ...]
    if PYTEST3_OR_GREATER:
        return tuple(m.mark for m in marks)
    elif len(marks) == 0:
        return ()
    else:
        return tuple(Mark(m.name, m.args, m.kwargs) for m in marks)
