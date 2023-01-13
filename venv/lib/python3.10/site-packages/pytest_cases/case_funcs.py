# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from copy import copy
from decopatch import function_decorator, DECORATED

try:  # python 3.5+
    from typing import Callable, Union, Optional, Any, Tuple, Iterable, List, Set
except ImportError:
    pass

from .common_mini_six import string_types
from .common_pytest import safe_isclass
from .common_pytest_marks import get_pytest_marks_on_function, markdecorators_as_tuple, markdecorators_to_markinfos

try:
    from _pytest.mark.structures import MarkDecorator, Mark
except ImportError:
    pass


# ------------------ API --------------
CASE_PREFIX_CLS = 'Case'
"""Prefix used by default to identify case classes"""

CASE_PREFIX_FUN = 'case_'
"""Prefix used by default to identify case functions within a module"""


CASE_FIELD = '_pytestcase'


class _CaseInfo(object):
    """
    Contains all information available about a case.
    It is attached to a case function as an attribute.

    Currently we do not wish to export an object-oriented API for this but rather a set of functions.
    This is why this class remains private. Public functions to access the various elements in this class
    are provided below (`get_case_id`, `get_case_tags` and `get_case_marks`). This is a safeguard to allow us
    to change this class design later while easily guaranteeing retrocompatibility.
    """
    __slots__ = ('id', 'marks', 'tags')

    def __init__(self,
                 id=None,   # type: str
                 marks=(),  # type: Tuple[MarkDecorator, ...]
                 tags=()    # type: Tuple[Any]
                 ):
        self.id = id
        self.marks = marks  # type: Tuple[MarkDecorator, ...]
        self.tags = ()
        self.add_tags(tags)

    def __repr__(self):
        return "_CaseInfo(id=%r,marks=%r,tags=%r)" % (self.id, self.marks, self.tags)

    @classmethod
    def get_from(cls,
                 case_func,               # type: Callable
                 create_if_missing=False  # type: bool
                 ):
        """ Return the _CaseInfo associated with case_fun or None

        :param case_func:
        :param create_if_missing: if no case information is present on the function, by default None is returned. If
            this flag is set to True, a new _CaseInfo will be created and attached on the function, and returned.
        """
        ci = getattr(case_func, CASE_FIELD, None)
        if ci is None and create_if_missing:
            ci = cls()
            ci.attach_to(case_func)
        return ci

    def attach_to(self,
                  case_func  # type: Callable
                  ):
        """attach this case_info to the given case function"""
        setattr(case_func, CASE_FIELD, self)

    def add_tags(self,
                 tags  # type: Union[Any, Union[List, Set, Tuple]]
                 ):
        """add the given tag or tags"""
        if tags:
            if isinstance(tags, string_types) or not isinstance(tags, (set, list, tuple)):
                # a single tag, create a tuple around it
                tags = (tags,)

            self.tags += tuple(tags)

    def matches_tag_query(self,
                          has_tag=None,  # type: Union[str, Iterable[str]]
                          ):
        """
        Returns True if the case function with this case_info is selected by the query

        :param has_tag:
        :return:
        """
        return _tags_match_query(self.tags, has_tag)

    @classmethod
    def copy_info(cls,
                  from_case_func,
                  to_case_func):
        case_info = cls.get_from(from_case_func)
        if case_info is not None:
            # there is something to copy: do it
            cp = copy(case_info)
            cp.attach_to(to_case_func)


def _tags_match_query(tags,    # type: Iterable[str]
                      has_tag  # type: Optional[Union[str, Iterable[str]]]
                      ):
    """Internal routine to determine is all tags in `has_tag` are persent in `tags`
    Note that `has_tag` can be a single tag, or none
    """
    if has_tag is None:
        return True

    if not isinstance(has_tag, (tuple, list, set)):
        has_tag = (has_tag,)

    return all(t in tags for t in has_tag)


def copy_case_info(from_fun,  # type: Callable
                   to_fun     # type: Callable
                   ):
    """Copy all information from case function `from_fun` to `to_fun`."""
    _CaseInfo.copy_info(from_fun, to_fun)


def set_case_id(id,        # type: str
                case_func  # type: Callable
                ):
    """Set an explicit id on case function `case_func`."""
    ci = _CaseInfo.get_from(case_func, create_if_missing=True)
    ci.id = id


def get_case_id(case_func,                              # type: Callable
                prefix_for_default_ids=CASE_PREFIX_FUN  # type: str
                ):
    """Return the case id associated with this case function.

    If a custom id is not present, a case id is automatically created from the function name based on removing the
    provided prefix if present at the beginning of the function name. If the resulting case id is empty,
    "<empty_case_id>" will be returned.

    :param case_func: the case function to get a case id for
    :param prefix_for_default_ids: this prefix that will be removed if present on the function name to form the default
        case id.
    :return:
    """
    _ci = _CaseInfo.get_from(case_func)
    _id = _ci.id if _ci is not None else None

    if _id is None:
        # default case id from function name based on prefix
        if case_func.__name__.startswith(prefix_for_default_ids):
            _id = case_func.__name__[len(prefix_for_default_ids):]
        else:
            _id = case_func.__name__

        # default case id for empty id
        if len(_id) == 0:
            _id = "<empty_case_id>"

    return _id


# def add_case_marks: no need, equivalent of @case(marks) or @mark


def get_case_marks(case_func,                         # type: Callable
                   concatenate_with_fun_marks=False,  # type: bool
                   as_decorators=False                # type: bool
                   ):
    # type: (...) -> Union[Tuple[Mark, ...], Tuple[MarkDecorator, ...]]
    """Return the marks that are on the case function.

    There are currently two ways to place a mark on a case function: either with `@pytest.mark.<name>` or in
    `@case(marks=...)`. This function returns a list of marks containing either both (if `concatenate_with_fun_marks` is
    `True`) or only the ones set with `@case` (`concatenate_with_fun_marks` is `False`, default).

    :param case_func: the case function
    :param concatenate_with_fun_marks: if `False` (default) only the marks declared in `@case` will be returned.
        Otherwise a concatenation of marks in `@case` and on the function (for example directly with
        `@pytest.mark.<name>`) will be returned.
    :param as_decorators: when `True`, the marks (`MarkInfo`) will be transformed into `MarkDecorators` before being
        returned. Otherwise (default) the marks are returned as is.
    :return:
    """
    _ci = _CaseInfo.get_from(case_func)
    if _ci is None:
        _ci_marks = None
    else:
        # convert the MarkDecorators to Marks if needed
        _ci_marks = _ci.marks if as_decorators else markdecorators_to_markinfos(_ci.marks)

    if not concatenate_with_fun_marks:
        return _ci_marks
    else:
        # concatenate the marks on the `_CaseInfo` with the ones on `case_func`
        fun_marks = tuple(get_pytest_marks_on_function(case_func, as_decorators=as_decorators))
        return (_ci_marks + fun_marks) if _ci_marks else fun_marks


# def add_case_tags(case_func,
#                   tags
#                   ):
#     """Adds tags on the case function, for filtering. This is equivalent to `@case(tags=...)(case_func)`"""
#     ci = _CaseInfo.get_from(case_func, create_if_missing=True)
#     ci.add_tags(tags)


def get_case_tags(case_func  # type: Callable
                  ):
    """Return the tags on this case function or an empty tuple"""
    ci = _CaseInfo.get_from(case_func)
    return ci.tags if ci is not None else ()


def matches_tag_query(case_fun,      # type: Callable
                      has_tag=None,  # type: Union[str, Iterable[str]]
                      filter=None,   # type: Union[Callable[[Callable], bool], Iterable[Callable[[Callable], bool]]]  # noqa
                      ):
    """
    This function is the one used by `@parametrize_with_cases` to filter the case functions collected. It can be used
    manually for tests/debug.

    Returns True if the case function is selected by the query:

     - if `has_tag` contains one or several tags, they should ALL be present in the tags
       set on `case_fun` (`get_case_tags`)

     - if `filter` contains one or several filter callables, they are all called in sequence and the
       `case_fun` is only selected if ALL of them return a `True` truth value

    :param case_fun: the case function
    :param has_tag: one or several tags that should ALL be present in the tags set on `case_fun` for it to be selected.
    :param filter: one or several filter callables that will be called in sequence. If all of them return a `True`
        truth value, `case_fun` is selected.
    :return: True if the case_fun is selected by the query.
    """
    selected = True

    # query on tags
    if has_tag is not None:
        selected = selected and _tags_match_query(get_case_tags(case_fun), has_tag)

    # filter function
    if filter is not None:
        if not isinstance(filter, (tuple, set, list)):
            filter = (filter,)

        for _filter in filter:
            # break if already unselected
            if not selected:
                return selected

            # try next filter
            try:
                res = _filter(case_fun)
                # keep this in the try catch in case there is an issue with the truth value of result
                selected = selected and res
            except:  # noqa
                # any error leads to a no-match
                selected = False

    return selected


try:
    SeveralMarkDecorators = Union[Tuple[MarkDecorator, ...], List[MarkDecorator], Set[MarkDecorator]]
except:  # noqa
    pass


@function_decorator
def case(id=None,             # type: str  # noqa
         tags=None,           # type: Union[Any, Iterable[Any]]
         marks=(),            # type: Union[MarkDecorator, SeveralMarkDecorators]
         case_func=DECORATED  # noqa
         ):
    """
    Optional decorator for case functions so as to customize some information.

    ```python
    @case(id='hey')
    def case_hi():
        return 1
    ```

    :param id: the custom pytest id that should be used when this case is active. Replaces the deprecated `@case_name`
        decorator from v1. If no id is provided, the id is generated from case functions by removing their prefix,
        see `@parametrize_with_cases(prefix='case_')`.
    :param tags: custom tags to be used for filtering in `@parametrize_with_cases(has_tags)`. Replaces the deprecated
        `@case_tags` and `@target` decorators.
    :param marks: optional pytest marks to add on the case. Note that decorating the function directly with the mark
        also works, and if marks are provided in both places they are merged.
    :return:
    """
    marks = markdecorators_as_tuple(marks)
    case_info = _CaseInfo(id, marks, tags)
    case_info.attach_to(case_func)
    return case_func


def is_case_class(cls,                                  # type: Any
                  case_marker_in_name=CASE_PREFIX_CLS,  # type: str
                  check_name=True                       # type: bool
                  ):
    """
    This function is the one used by `@parametrize_with_cases` to collect cases within classes. It can be used manually
    for tests/debug.

    Returns True if the given object is a class and, if `check_name=True` (default), if its name contains
    `case_marker_in_name`.

    :param cls: the object to check
    :param case_marker_in_name: the string that should be present in a class name so that it is selected. Default is
        'Case'.
    :param check_name: a boolean (default True) to enforce that the name contains the word `case_marker_in_name`.
        If False, any class will lead to a `True` result whatever its name.
    :return: True if this is a case class
    """
    return safe_isclass(cls) and (not check_name or case_marker_in_name in cls.__name__)


GEN_BY_US = '_pytestcases_gen'


def is_case_function(f,                       # type: Any
                     prefix=CASE_PREFIX_FUN,  # type: str
                     check_prefix=True        # type: bool
                     ):
    """
    This function is the one used by `@parametrize_with_cases` to collect cases. It can be used manually for
    tests/debug.

    Returns True if the provided object is a function or callable and, if `check_prefix=True` (default), if it starts
    with `prefix`.

    :param f: the object to check
    :param prefix: the string that should be present at the beginning of a function name so that it is selected.
        Default is 'case_'.
    :param check_prefix: if this boolean is True (default), the prefix will be checked. If False, any function will
        lead to a `True` result whatever its name.
    :return:
    """
    if not callable(f):
        return False
    elif safe_isclass(f):
        return False
    elif hasattr(f, GEN_BY_US):
        # a function generated by us. ignore this
        return False
    else:
        return f.__name__.startswith(prefix) if check_prefix else True
