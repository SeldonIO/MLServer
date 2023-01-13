# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
import re

from .case_funcs import get_case_id, get_case_tags


class CaseFilter(object):
    """
    This class represents a case filter. You can use it in order to filter cases to be used by `parametrize_by_cases`.

    `CaseFilter` implements logical operations "and" (`&`) "or" (`|`) and "not" (`~`). You can use it to define a
    composable filter from any callable receiving a single `case` argument and returning a boolean indicating if the
    `case` is selected.
    """

    def __init__(self, filter_function):
        self.filter_function = filter_function

    def __call__(self, case):
        return self.filter_function(case)

    def __and__(self, other):
        return CaseFilter(
            lambda case: self(case) and other(case)
        )

    def __rand__(self, other):
        return self & other

    def __or__(self, other):
        return CaseFilter(
            lambda case: self(case) or other(case)
        )

    def __ror__(self, other):
        return self | other

    def __invert__(self):
        return CaseFilter(
            lambda case: not self(case)
        )


def has_tags(*tag_names  # type: str
             ):
    """
    Selects cases that have all tags in `tag_names`. See `@case(tags=...)` to add tags to a case.

    :param tag_names:
    :return:
    """

    def _filter(case):
        return len(
            set(tag_names) - set(get_case_tags(case))
        ) == 0

    return CaseFilter(_filter)


def has_tag(tag_name  # type: str
            ):
    """
    Selects cases that have the tag `tag_name`. See `@case(tags=...)` to add tags to a case.

    :param tag_name:
    :return:
    """

    def _filter(case):
        return tag_name in get_case_tags(case)

    return CaseFilter(_filter)


def id_has_prefix(prefix  # type: str
                  ):
    """
    Selects cases that have a case id prefix `prefix`.

    Note that this is not the prefix of the whole case function name, but the case id,
    possibly overridden with `@case(id=)`
    """

    def _filter(case):
        return get_case_id(case).startswith(prefix)

    return CaseFilter(_filter)


def id_has_suffix(suffix  # type: str
                  ):
    """
    Selects cases that have a case id suffix `suffix`.

    Note that this is not the suffix of the whole case function name, but the case id,
    possibly overridden with `@case(id=)`
    """

    def _filter(case):
        return get_case_id(case).endswith(suffix)

    return CaseFilter(_filter)


def id_match_regex(regex  # type: str
                   ):
    """
    Select cases that have a case id matching `regex`.

    Note that this is not a match of the whole case function name, but the case id,
    possibly overridden with `@case(id=)`
    """

    def _filter(case):
        return re.match(regex, get_case_id(case))

    return CaseFilter(_filter)
