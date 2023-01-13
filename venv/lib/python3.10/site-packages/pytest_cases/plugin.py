# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from collections import OrderedDict, namedtuple
from copy import copy
from functools import partial
from warnings import warn

try:
    from collections.abc import MutableSequence
except:  # noqa
    from collections import MutableSequence

import pytest

try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature  # noqa

try:  # python 3.3+ type hints
    from typing import List, Tuple, Union, Iterable, MutableMapping, Mapping, Optional  # noqa
    from _pytest.python import CallSpec2
    from _pytest.config import Config
except ImportError:
    pass

from .common_mini_six import string_types
from .common_pytest_lazy_values import get_lazy_args
from .common_pytest_marks import PYTEST35_OR_GREATER, PYTEST46_OR_GREATER, PYTEST37_OR_GREATER, PYTEST7_OR_GREATER
from .common_pytest import get_pytest_nodeid, get_pytest_function_scopeval, is_function_node, get_param_names, \
    get_param_argnames_as_list, has_function_scope, set_callspec_arg_scope_to_function

from .fixture_core1_unions import NOT_USED, USED, is_fixture_union_params, UnionFixtureAlternative

# if PYTEST54_OR_GREATER:
#     # we will need to clean the empty ids explicitly in the plugin :'(
from .fixture_parametrize_plus import remove_empty_ids

from .case_parametrizer_new import get_current_cases


_DEBUG = False


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_pycollect_makeitem(collector, name, obj):
#     # custom collection of additional things - we could use it one day for Cases ?
#     # see also https://hackebrot.github.io/pytest-tricks/customize_class_collection/
#     outcome = yield
#     res = outcome.get_result()
#     if res is not None:
#         return
#     # nothing was collected elsewhere, let's do it here
#     if safe_isclass(obj):
#         if collector.istestclass(obj, name):
#             outcome.force_result(Class(name, parent=collector))
#     elif collector.istestfunction(obj, name):
#         ...


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """ Resolve all `lazy_value` in the dictionary of function args """

    yield  # first let all other hooks run, they will do the setup etc.

    # now item.funcargs exists so we can handle it
    if hasattr(item, "funcargs"):
        item.funcargs = {argname: get_lazy_args(argvalue, item)
                         for argname, argvalue in item.funcargs.items()}


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_collection(session):
    """ HACK: override the fixture manager's `getfixtureclosure` method to replace it with ours """

    # Note for reference: another way to access the fm is `metafunc.config.pluginmanager.get_plugin('funcmanage')`
    session._fixturemanager.getfixtureclosure = partial(getfixtureclosure, session._fixturemanager)  # noqa


class FixtureDefsCache(object):
    """
    A 'cache' for fixture definitions obtained from the FixtureManager `fm`, for test node `nodeid`
    """
    __slots__ = 'fm', 'nodeid', 'cached_fix_defs'

    def __init__(self, fm, nodeid):
        self.fm = fm
        self.nodeid = nodeid
        self.cached_fix_defs = dict()

    def get_fixture_defs(self, fixname):
        try:
            # try to retrieve it from cache
            fixdefs = self.cached_fix_defs[fixname]
        except KeyError:
            # otherwise get it and store for next time
            fixdefs = self.fm.getfixturedefs(fixname, self.nodeid)
            self.cached_fix_defs[fixname] = fixdefs

        return fixdefs


class FixtureClosureNode(object):
    """
    A node in a fixture closure Tree.

     - its `fixture_defs` is a {name: def} ordered dict containing all fixtures AND args that are required at this node
       (*before* a union is required). Note that some of them have def=None when the fixture manager has no definition
       for them (same beahviour than in pytest). `get_all_fixture_names` and `get_all_fixture_defs` helper functions
       allow to either return the full ordered list (equivalent to pytest `fixture_names`) or the dictionary of non-none
       definitions (equivalent to pytest `arg2fixturedefs`)

     - if a union appears at this node, `split_fixture_name` is set to the name of the union fixture, and `children`
       contains an ordered dict of {split_fixture_alternative: node}

    """
    __slots__ = 'parent', 'fixture_defs_mgr', \
                'fixture_defs', 'split_fixture_name', 'split_fixture_alternatives', 'children'

    def __init__(self,
                 fixture_defs_mgr=None,   # type: FixtureDefsCache
                 parent_node=None         # type: FixtureClosureNode
                 ):
        if fixture_defs_mgr is None:
            if parent_node is None:
                raise ValueError("root node should have a fixture defs manager")
            fixture_defs_mgr = parent_node.fixture_defs_mgr
        else:
            assert isinstance(fixture_defs_mgr, FixtureDefsCache)

        self.fixture_defs_mgr = fixture_defs_mgr
        self.parent = parent_node

        # these will be set after closure has been built
        self.fixture_defs = None  # type: OrderedDict
        self.split_fixture_name = None  # type: str
        self.split_fixture_alternatives = []
        # we do not use a dict any more as several children can use the same union value (doubled unions)
        self.children = []  # type: List[FixtureClosureNode]

    # ------ tree ------------------

    def get_leaves(self):
        if self.has_split():
            return [n for c in self.children for n in c.get_leaves()]
        else:
            return [self]

    # ------ str / repr ---------------

    def to_str(self, indent_nb=0, with_children=True):
        """  a string representation, either with all the subtree (default) or without (with_children=False) """

        indent = " " * indent_nb

        if not self.is_closure_built():
            str_repr = "<pending, incomplete>"
        else:
            str_repr = "%s(%s)" % (indent, ",".join([("%s" % f) for f in self.fixture_defs.keys()]))

        if self.has_split() and with_children:
            children_str_prefix = "\n%s - " % indent
            children_str = children_str_prefix + children_str_prefix.join([c.to_str(indent_nb=indent_nb + 1)
                                                                           for c in self.children])
            str_repr = str_repr + " split: " + self.split_fixture_name + children_str

        return str_repr

    def __repr__(self):
        return self.to_str()

    # ---- getters to read the "super" closure (used in SuperClosure)

    def get_all_fixture_names(self, try_to_sort_by_scope=True):
        """ Return a list containing all unique fixture names used by this tree"""
        if not try_to_sort_by_scope:
            return [k for k, _ in self.gen_all_fixture_defs(drop_fake_fixtures=False)]
        else:
            return list(self.get_all_fixture_defs(drop_fake_fixtures=False, try_to_sort=True))

    def get_all_fixture_defs(self, drop_fake_fixtures=True, try_to_sort=True):
        """ Return a dict containing all fixture definitions for fixtures used in this tree"""
        # get all pairs
        items = self.gen_all_fixture_defs(drop_fake_fixtures=drop_fake_fixtures)

        # sort by scope as in pytest fixture closure creator (pytest did not do it in early versions, align with this)
        if try_to_sort:
            if PYTEST7_OR_GREATER:
                # Scope is an enum, values are in reversed order, and the field is _scope
                f_scope = get_pytest_function_scopeval()

                def sort_by_scope(kv_pair):
                    fixture_name, fixture_defs = kv_pair
                    return fixture_defs[-1]._scope if fixture_defs is not None else f_scope
                items = sorted(list(items), key=sort_by_scope, reverse=True)

            elif PYTEST35_OR_GREATER:
                # scopes is a list, values are indices in the list, and the field is scopenum
                f_scope = get_pytest_function_scopeval()
                def sort_by_scope(kv_pair):  # noqa
                    fixture_name, fixture_defs = kv_pair
                    return fixture_defs[-1].scopenum if fixture_defs is not None else f_scope
                items = sorted(list(items), key=sort_by_scope)

        return OrderedDict(items)

    def gen_all_fixture_defs(self, drop_fake_fixtures=True):
        """
        Generate all pairs of (fixture name, fixture def or none) used in the tree in top to bottom order
        Note that this method could be generalized to also yield the parent defs, so as to be used to replace
        the engine in `self.gather_all_required`. But this is micro-optimization, really.
        Note: `gather_all_required` was not built to be concerned with ordering because it is only used as a set.
        """

        # fixtures required at this node
        for k, v in self.fixture_defs.items():
            if not drop_fake_fixtures or v is not None:
                yield k, v

        # split fixture: not needed since it is the last entry in self.fixture_defs

        # fixtures required by children if any
        for c in self.children:
            for k, v in c.gen_all_fixture_defs(drop_fake_fixtures=drop_fake_fixtures):
                yield k, v

    # ---- utils to build the closure

    def build_closure(self,
                      initial_fixture_names,  # type: Iterable[str]
                      ignore_args=()
                      ):
        """
        Updates this Node with the fixture names provided as argument.
        Fixture names and definitions will be stored in self.fixture_defs.

        If some fixtures are Union fixtures, this node will become a "split" node
        and have children. If new fixtures are added to the node after that,
        they will be added to the child nodes rather than self.

        :param initial_fixture_names:
        :param ignore_args: arguments to keep in the names but not to put in the fixture defs, because they correspond
            to "direct parametrization"
        :return:
        """
        self._build_closure(self.fixture_defs_mgr, initial_fixture_names, ignore_args=ignore_args)

    def is_closure_built(self):
        return self.fixture_defs is not None

    def already_knows_fixture(self, fixture_name):
        """ Return True if this fixture is known by this node or one of its parents """
        if fixture_name in self.fixture_defs:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.already_knows_fixture(fixture_name)

    def _build_closure(self,
                       fixture_defs_mgr,       # type: FixtureDefsCache
                       initial_fixture_names,  # type: Iterable[str]
                       ignore_args
                       ):
        """

        :param fixture_defs_mgr:
        :param initial_fixture_names:
        :param ignore_args: arguments to keep in the names but not to put in the fixture defs
        :return: nothing (the input arg2fixturedefs is modified)
        """

        # Grab all dependencies of all fixtures present at this node and add them to either this or to nodes below.

        # -- first switch this object from 'pending' to 'under construction' if needed
        # (indeed we now authorize and use the possibility to call this twice. see split() )
        if self.fixture_defs is None:
            self.fixture_defs = OrderedDict()

        # -- then for all pending, add them with their dependencies
        pending_fixture_names = list(initial_fixture_names)
        while len(pending_fixture_names) > 0:
            fixname = pending_fixture_names.pop(0)

            # if the fixture is already known in this node or above, do not care
            if self.already_knows_fixture(fixname):
                continue

            # new ignore_args option in pytest 4.6+. Not really a fixture but a test function parameter, it seems.
            if fixname in ignore_args:
                self.add_required_fixture(fixname, None)
                continue

            # else grab the fixture definition(s) for this fixture name for this test node id
            fixturedefs = fixture_defs_mgr.get_fixture_defs(fixname)
            if not fixturedefs:
                # fixture without definition: add it. This can happen with e.g. "requests", etc.
                self.add_required_fixture(fixname, None)
                continue
            else:
                # the actual definition is the last one
                _fixdef = fixturedefs[-1]
                _params = _fixdef.params

                if _params is not None and is_fixture_union_params(_params):
                    # create an UNION fixture

                    # transform the _params into a list of names
                    alternative_f_names = UnionFixtureAlternative.to_list_of_fixture_names(_params)

                    # TO DO if only one name, simplify ? >> No, we leave such "optimization" to the end user

                    # if there are direct dependencies that are not the union members, add them to pending
                    non_member_dependencies = [f for f in _fixdef.argnames if f not in alternative_f_names]
                    # currently we only have 'requests' in this list but future impl of fixture_union may act otherwise
                    pending_fixture_names += non_member_dependencies

                    # propagate WITH the pending
                    self.split_and_build(fixture_defs_mgr, fixname, fixturedefs, alternative_f_names,
                                         pending_fixture_names, ignore_args=ignore_args)

                    # empty the pending because all of them have been propagated on all children with their dependencies
                    pending_fixture_names = []
                    continue

                else:
                    # normal fixture
                    self.add_required_fixture(fixname, fixturedefs)

                    # add all dependencies in the to do list
                    dependencies = _fixdef.argnames
                    # - append: was pytest default
                    # pending_fixture_names += dependencies
                    # - prepend: makes much more sense
                    pending_fixture_names = list(dependencies) + pending_fixture_names
                    continue

    # ------ tools to add new fixture names during closure construction

    # def prepend_fixture_without_dependencies(self, fixname):
    #     """"""
    #     fixturedefs = self.fixture_defs_mgr.get_fixture_defs(fixname)
    #     if not fixturedefs:
    #         # fixture without definition: add it. This can happen with e.g. "requests", etc.
    #         self.fixture_defs.insert((fixname, None))
    #     else:
    #         # the actual definition is the last one
    #         _fixdef = fixturedefs[-1]
    #         _params = _fixdef.params
    #
    #         if _params is not None and is_fixture_union_params(_params):
    #             # union fixture
    #             raise ValueError("It is not possible to add a union fixture after the initial closure has been built")
    #         else:
    #             # normal fixture
    #             self.add_required_fixture(fixname, fixturedefs)
    #
    #             # add all dependencies in the to do list
    #             dependencies = _fixdef.argnames

    # def add_fixture_without_dependencies(self, fixname):
    #     """Used for later addition, once the closure has been built"""
    #     fixturedefs = self.fixture_defs_mgr.get_fixture_defs(fixname)
    #     if not fixturedefs:
    #         # fixture without definition: add it. This can happen with e.g. "requests", etc.
    #         self.add_required_fixture(fixname, None)
    #     else:
    #         # the actual definition is the last one
    #         _fixdef = fixturedefs[-1]
    #         _params = _fixdef.params
    #
    #         if _params is not None and is_fixture_union_params(_params):
    #             # union fixture
    #             raise ValueError("It is not possible to add a union fixture after the initial closure has been built")
    #         else:
    #             # normal fixture
    #             self.add_required_fixture(fixname, fixturedefs)

    def remove_fixtures(self, fixture_names_to_remove):
        """Remove some fixture names from all nodes in this subtree. These fixtures should not be split fixtures"""
        _to_remove_in_children = []
        for f in fixture_names_to_remove:
            if self.split_fixture_name == f:
                raise NotImplementedError("It is not currently possible to remove a split fixture name from a closure "
                                          "with splits")
            try:
                del self.fixture_defs[f]
            except KeyError:
                _to_remove_in_children.append(f)

        # propagate to children if any
        if len(_to_remove_in_children) > 0:
            for c in self.children:
                c.remove_fixtures(_to_remove_in_children)

    def add_required_fixture(self, new_fixture_name, new_fixture_defs):
        """Add some required fixture names to all leaves under this node"""
        if self.already_knows_fixture(new_fixture_name):
            return
        elif not self.has_split():
            # add_required_fixture locally
            if new_fixture_name not in self.fixture_defs:
                self.fixture_defs[new_fixture_name] = new_fixture_defs
        else:
            # add_required_fixture in each child
            for c in self.children:
                c.add_required_fixture(new_fixture_name, new_fixture_defs)

    def split_and_build(self,
                        fixture_defs_mgr,           # type: FixtureDefsCache
                        split_fixture_name,         # type: str
                        split_fixture_defs,         # type: Tuple[FixtureDefinition]  # noqa
                        alternative_fixture_names,  # type: List[str]
                        pending_fixtures_list,      #
                        ignore_args
                        ):
        """ Declares that this node contains a union with alternatives (child nodes=subtrees) """

        if self.has_split():
            raise ValueError("This should not happen anymore")
            # # propagate the split on the children: split each of them
            # for n in self.children:
            #     n.split_and_build(fm, nodeid, split_fixture_name, split_fixture_defs, alternative_fixture_names)
        else:
            # add the split (union) name to known fixtures
            self.add_required_fixture(split_fixture_name, split_fixture_defs)

            # remember it
            self.split_fixture_name = split_fixture_name
            self.split_fixture_alternatives = alternative_fixture_names

            # create the child nodes
            for f in alternative_fixture_names:
                # create the child node
                new_c = FixtureClosureNode(parent_node=self)
                self.children.append(new_c)

                # set the discarded fixture names
                # new_c.split_fixture_discarded_names = [g for g in alternative_fixture_names if g != f]

                # perform the propagation:
                # (a) first propagate all child's dependencies, (b) then the ones required by parent
                # we need to do both at the same time in order to propagate the "pending for child" on all subbranches
                pending_for_child = [f] + pending_fixtures_list
                new_c._build_closure(fixture_defs_mgr, pending_for_child, ignore_args=ignore_args)

    def has_split(self):
        return self.split_fixture_name is not None

    # ----------- for calls parametrization

    def get_not_always_used(self):
        """Return the list of fixtures used by this subtree, that are used in *some* leaves only, not all"""
        results_list = []

        # initial list is made of fixtures that are in the children
        initial_list = self.gather_all_required(include_parents=False)

        for c in self.get_leaves():
            j = 0
            for _ in range(len(initial_list)):
                # get next element in the list (but the list may reduce in size during the loop)
                fixture_name = initial_list[j]
                if fixture_name not in c.gather_all_required():
                    # Remove element from the list. Therefore, do not increment j
                    del initial_list[j]
                    results_list.append(fixture_name)
                else:
                    # Do not remove from the list: increment j
                    j += 1

        return results_list

    def gather_all_required(self, include_children=True, include_parents=True):
        """
        Return a list of all fixtures required by the subtree containing this node
        and all of its parents (if include_parents=True) and all of its children (if include_children=True)

        See also `self.gen_all_fixture_defs`, that could be generalized to tackle this use case too
        (micro-optimization, not really urgent)
        """
        # first the fixtures required by this node
        required = list(self.fixture_defs.keys())

        # then the ones required by the parents
        if include_parents and self.parent is not None:
            required = required + self.parent.gather_all_required(include_children=False)

        # then the ones from all the children
        if include_children:
            for child in self.children:
                required = required + child.gather_all_required(include_parents=False)

        return required

    def requires(self, fixturename):
        """ Return True if the fixture with this name is required by the subtree at this node """
        return fixturename in self.gather_all_required()

    # ------ tools to see the tree as a list of alternatives (used in SuperClosure)

    def get_alternatives(self):
        """
        Returns the tree  "flattened" as a list of alternatives (one per leaf).
        Each entry in the list consists of:

         - an ordered dictionary {union_fixture_name: (idx, value)} representing the active union filters in this
           alternative
         - a list of fixture names effectively used in this alternative

        :return: a list of alternatives
        """
        alternatives = self._get_alternatives()
        for i, a in enumerate(alternatives):
            # replace the first entry in the tuple with a reversed order one
            alternatives[i] = (OrderedDict(reversed(list(a[0].items()))), a[1])
        return alternatives

    def _get_alternatives(self):
        if self.has_split():
            alternatives_list = []
            for c_idx, (c_split_alternative, c_node) in enumerate(zip(self.split_fixture_alternatives, self.children)):
                # for all alternatives in this subtree
                for f_dct, n_lst in c_node._get_alternatives():
                    # - filter
                    _f_dct = f_dct.copy()
                    _f_dct[self.split_fixture_name] = (c_idx, c_split_alternative)

                    # - unique fixtures used
                    _n_lst = list(self.fixture_defs) + [_i for _i in n_lst if _i not in self.fixture_defs]

                    alternatives_list.append((_f_dct, _n_lst))

            return alternatives_list
        else:
            # return a single partition containing no filter and all fixture names
            return [(OrderedDict(), self.get_all_fixture_names())]


class SuperClosure(MutableSequence):
    """
    A "super closure" is a closure made of several closures, each induced by a fixture union parameter value.
    The number of alternative closures is `self.nb_alternative_closures`

    This object behaves like a list (a mutable sequence), so that we can pass it to pytest in place of the list of
    fixture names that is returned in `getfixtureclosure`.

    In this implementation, it is backed by a fixture closure tree, that we have to preserve in order to get
    parametrization right. In another branch of this project ('super_closure' branch) we tried to forget the tree
    and only keep the partitions, but parametrization order was not as intuitive for the end user as all unions
    appeared as parametrized first (since they induced the partitions).
    """
    __slots__ = 'tree', 'all_fixture_defs'

    def __init__(self,
                 root_node  # type: FixtureClosureNode
                 ):
        # if we wish to drop the tree - but we do not anymore to get a better paramz order
        # filters_list, partitions_list = root_node._get_alternatives()

        # save the fixture closure tree root
        self.tree = root_node
        # retrieve/sort fixture defs for quicker access
        self._update_fixture_defs()

    def _update_fixture_defs(self):
        # get a list of all fixture defs, for quicker access (and sorted)
        # sort by scope as in pytest fixture closure creator, if scope information is available
        all_fixture_defs = self.tree.get_all_fixture_defs(drop_fake_fixtures=False, try_to_sort=True)

        # # also sort all partitions (note that we cannot rely on the order in all_fixture_defs when scopes are same!)
        # if LooseVersion(pytest.__version__) >= LooseVersion('3.5.0'):
        #     f_scope = get_pytest_function_scopeval()
        #     for p in self.partitions:
        #         def sort_by_scope2(fixture_name):  # noqa
        #             fixture_defs = all_fixture_defs[fixture_name]
        #             return fixture_defs[-1].scopenum if fixture_defs is not None else f_scope
        #         p.sort(key=sort_by_scope2)

        self.all_fixture_defs = all_fixture_defs

    # --- visualization tools ----

    @property
    def nb_alternative_closures(self):
        """ Return the number of alternative closures induced by fixture unions """
        filters, partitions = self.tree.get_alternatives()
        return len(partitions)

    def __repr__(self):
        """ Return a synthetic view, and a detailed tree view, of this closure """
        alternatives = self.tree.get_alternatives()
        nb_alternative_closures = len(alternatives)
        return "SuperClosure with %s alternative closures:\n" % nb_alternative_closures \
               + "\n".join(" - %s (filters: %s)" % (p, ", ".join("%s=%s[%s]=%s" % (k, k, v[0], v[1])
                                                                 for k, v in f.items()))
                           for f, p in alternatives) \
               + "\nThe 'super closure list' is %s\n\nThe fixture tree is :\n%s\n" % (list(self), self.tree)

    def get_all_fixture_defs(self, drop_fake_fixtures=True):
        """
        Return a dictionary of all fixture defs used in this super closure

        note: this is equivalent to
        self.tree.get_all_fixture_defs(drop_fake_fixtures=drop_fake_fixtures, try_to_sort=True)
        """
        if drop_fake_fixtures:
            # remove the "fixtures" that are actually test function parameter args
            return {k: v for k, v in self.all_fixture_defs.items() if v is not None}
        else:
            # all fixtures AND pseudo-fixtures (test function parameters)
            return self.all_fixture_defs

    # ---- list (MutableSequence) facade: behaves like a list of fixture names ------

    def __len__(self):
        return len(self.all_fixture_defs)

    def __getitem__(self, i):
        # return the key (fixture name) associated with the i-th pair
        # try:
        #     return next(islice(self.all_fixture_defs.keys(), i, i+1))
        # except StopIteration:
        #     raise IndexError(i)
        return list(self.all_fixture_defs.keys())[i]

    def __setitem__(self, i, o):
        # try:
        #     # pytest performs a full replacement using [:] so we handle at least this case
        #     full_replace = i == slice(None, None, None)
        # except:  # noqa
        #     full_replace = False

        # Get the existing value(s) that we wish to replace
        ref = list(self)[i]

        if o == ref:
            # no change at all: of course we accept.
            return

        if not isinstance(i, slice):
            # In-place change of a single item: let's be conservative and reject for now
            # if i == 0:
            #     self.remove(ref)
            #     self.insert(0, o)
            # elif i == len(self) - 1:
            #     self.remove(ref)
            #     self.append(o)
            # else:
            raise NotImplementedError("Replacing an element in a super fixture closure is not currently implemented. "
                                      "Please report this issue to the `pytest-cases` project.")
        else:
            # Replacement of multiple items at once: support reordering (ignored) and removal (actually done)
            new_set = set(o)
            ref_set = set(ref)
            if new_set == ref_set:
                # A change is required in the order of fixtures. Ignore but continue
                warn("WARNING: An attempt was made to reorder a super fixture closure with unions. This is not yet "
                     "supported since the partitions use subsets of the fixtures ; please report it so that we can "
                     "find a suitable solution for your need.")
                return

            added = new_set.difference(ref_set)
            removed = ref_set.difference(new_set)
            if len(added) == 0:
                # Pure removal: ok.
                self.remove_all(removed)
                return
            else:
                # self.append_all(added)
                # Rather be conservative for now
                raise NotImplementedError("Adding elements to a super fixture closure with a slice is not currently"
                                          "implemented. Please report this issue to the `pytest-cases` project.")

    def __delitem__(self, i):
        self.remove(self[i])

    def insert(self, index, fixture_name):
        """
        Try to transparently support inserts. Since the underlying structure is a tree, only two cases
        are supported: inserting at position 0 and appending at position len(self).

        Note that while appending has no restrictions, inserting at position 0 is only allowed for now if the
        fixture to insert does not have a union in its associated closure.

        :param index:
        :param fixture_name:
        :return:
        """
        if index == 0:
            # build the closure associated with this new fixture name
            fixture_defs_mgr = FixtureDefsCache(self.tree.fixture_defs_mgr.fm, self.tree.fixture_defs_mgr.nodeid)
            closure_tree = FixtureClosureNode(fixture_defs_mgr=fixture_defs_mgr)
            closure_tree.build_closure((fixture_name,))
            if closure_tree.has_split():
                raise NotImplementedError("When fixture unions are present, inserting a fixture in the closure at "
                                          "position 0 is currently only supported if that fixture's closure does not"
                                          "contain a union. Please report this so that we can find a suitable solution"
                                          " for your need.")
            else:
                # remove those fixture definitions from all nodes in the tree
                self.tree.remove_fixtures(closure_tree.fixture_defs.keys())

                # finally prepend the defs at the beginning of the dictionnary in the first node
                self.tree.fixture_defs = OrderedDict(list(closure_tree.fixture_defs.items())
                                                     + list(self.tree.fixture_defs.items()))

        elif index == len(self):
            # appending is natively supported in our tree growing method
            self.tree.build_closure((fixture_name,))
        else:
            raise NotImplementedError("When fixture unions are present, inserting a fixture in the closure at a "
                                      "position different from 0 (prepend) or <end> (append) is non-trivial. Please"
                                      "report this so that we can find a suitable solution for your need.")

        # Finally update self.fixture_defs so that the "list" view reflects the changes in self.tree
        self._update_fixture_defs()

    def append_all(self, fixture_names):
        """Append various fixture names to the closure"""
        # appending is natively supported in our tree growing method
        self.tree.build_closure(tuple(fixture_names))

        # Finally update self.fixture_defs so that the "list" view reflects the changes in self.tree
        self._update_fixture_defs()

    def remove(self, value):
        """
        Try to transparently support removal. Note: since the underlying structure is a tree,
        removing "union" fixtures is non-trivial so for now it is not supported.

        :param value:
        :return:
        """
        # remove in the tree
        self.tree.remove_fixtures((value,))

        # update fixture defs
        self._update_fixture_defs()

    def remove_all(self, values):
        """Multiple `remove` operations at once."""
        # remove in the tree
        self.tree.remove_fixtures(tuple(values))

        # update fixture defs
        self._update_fixture_defs()


def getfixtureclosure(fm, fixturenames, parentnode, ignore_args=()):
    """
    Replaces pytest's getfixtureclosure method to handle unions.
    """

    # (1) first retrieve the normal pytest output for comparison
    kwargs = dict()
    if PYTEST46_OR_GREATER:
        # new argument "ignore_args" in 4.6+
        kwargs['ignore_args'] = ignore_args

    if PYTEST37_OR_GREATER:
        # three outputs
        initial_names, ref_fixturenames, ref_arg2fixturedefs = \
            fm.__class__.getfixtureclosure(fm, fixturenames, parentnode, **kwargs)
    else:
        # two outputs
        ref_fixturenames, ref_arg2fixturedefs = fm.__class__.getfixtureclosure(fm, fixturenames, parentnode)

    # (2) now let's do it by ourselves to support fixture unions
    _init_fixnames, super_closure, arg2fixturedefs = create_super_closure(fm, parentnode, fixturenames, ignore_args)

    # Compare with the previous behaviour TODO remove when in 'production' ?
    # NOTE different order happens all the time because of our "prepend" strategy in the closure building
    # which makes much more sense/intuition than pytest default
    assert set(super_closure) == set(ref_fixturenames)
    assert dict(arg2fixturedefs) == ref_arg2fixturedefs

    if PYTEST37_OR_GREATER:
        return _init_fixnames, super_closure, arg2fixturedefs
    else:
        return super_closure, arg2fixturedefs


def create_super_closure(fm,
                         parentnode,
                         fixturenames,
                         ignore_args
                         ):
    # type: (...) -> Tuple[List, Union[List, SuperClosure], Mapping]
    """

    :param fm:
    :param parentnode:
    :param fixturenames:
    :param ignore_args:
    :return:
    """

    parentid = parentnode.nodeid

    if _DEBUG:
        print("Creating closure for %s:" % parentid)

    # -- auto-use fixtures
    _init_fixnames = list(fm._getautousenames(parentid))  # noqa

    def _merge(new_items, into_list):
        """ Appends items from `new_items` into `into_list`, only if they are not already there. """
        for item in new_items:
            if item not in into_list:
                into_list.append(item)

    # -- required fixtures/params.
    # ********* fix the order of initial fixtures: indeed this order may not be the right one ************
    # this only works when pytest version is > 3.4, otherwise the parent node is a Module
    if is_function_node(parentnode):
        # grab all the parametrization on that node and fix the order.
        # Note: on pytest >= 4 the list of param_names is probably the same than the `ignore_args` input
        param_names = get_param_names(parentnode)

        sorted_fixturenames = sort_according_to_ref_list(fixturenames, param_names)
        # **********
        # merge the fixture names in correct order into the _init_fixnames
        _merge(sorted_fixturenames, _init_fixnames)
    else:
        # we cannot sort yet - merge the fixture names into the _init_fixnames
        _merge(fixturenames, _init_fixnames)

    # Finally create the closure
    fixture_defs_mgr = FixtureDefsCache(fm, parentid)
    closure_tree = FixtureClosureNode(fixture_defs_mgr=fixture_defs_mgr)
    closure_tree.build_closure(_init_fixnames, ignore_args=ignore_args)
    super_closure = SuperClosure(closure_tree)
    all_fixture_defs = super_closure.get_all_fixture_defs(drop_fake_fixtures=True)

    # possibly simplify into a list
    if not closure_tree.has_split():
        super_closure = list(super_closure)

    if _DEBUG:
        print("Closure for %s completed:" % parentid)
        print(closure_tree)
        print(super_closure)

    return _init_fixnames, super_closure, all_fixture_defs


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_generate_tests(metafunc):
    """
    We use this hook to replace the 'partial' function of `metafunc` with our own below, before it is called by pytest
    Note we could do it in a static way in pytest_sessionstart or plugin init hook but
    that way we can still access the original method using metafunc.__class__.parametrize
    """
    # override the parametrize method.
    metafunc.parametrize = partial(parametrize, metafunc)

    # now let pytest parametrize the call as usual
    _ = yield


class UnionParamz(namedtuple('UnionParamz', ['union_fixture_name', 'alternative_names', 'ids', 'scope', 'kwargs'])):
    """ Represents some parametrization to be applied, for a union fixture """

    __slots__ = ()

    def __str__(self):
        return "[UNION] %s=[%s], ids=%s, scope=%s, kwargs=%s" \
               "" % (self.union_fixture_name, ','.join([str(a) for a in self.alternative_names]),
                     self.ids, self.scope, self.kwargs)


class NormalParamz(namedtuple('NormalParamz', ['argnames', 'argvalues', 'indirect', 'ids', 'scope', 'kwargs'])):
    """ Represents some parametrization to be applied """

    __slots__ = ()

    def __str__(self):
        return "[NORMAL] %s=[%s], indirect=%s, ids=%s, scope=%s, kwargs=%s" \
               "" % (self.argnames, self.argvalues, self.indirect, self.ids, self.scope, self.kwargs)


def parametrize(metafunc, argnames, argvalues, indirect=False, ids=None, scope=None, **kwargs):
    """
    This alternate implementation of metafunc.parametrize creates a list of calls that is not just the cartesian
    product of all parameters (like the pytest behaviour). Instead, it offers an alternate list of calls taking into
    account all "union" fixtures.

    For this, it replaces the `metafunc._calls` attribute with a `CallsReactor` instance, and feeds it with all
    parameters and parametrized fixtures independently (not doing any cross-product during this call). The resulting
    `CallsReactor` instance is then able to dynamically behave like the correct list of calls, lazy-creating that list
    when it is used.
    """
    if not isinstance(metafunc.fixturenames, SuperClosure):
        # legacy method
        metafunc.__class__.parametrize(metafunc, argnames, argvalues, indirect=indirect, ids=ids, scope=scope, **kwargs)

        # clean EMPTY_ID : since they are never set by us in a normal parametrize, no need to do this here.
        # if PYTEST54_OR_GREATER:
        #     for callspec in metafunc._calls:
        #         remove_empty_ids(callspec)
    else:
        # get or create our special container object
        if not isinstance(metafunc._calls, CallsReactor):  # noqa
            # first call: should be an empty list
            if len(metafunc._calls) > 0:  # noqa
                raise ValueError("This should not happen - please file an issue")
            metafunc._calls = CallsReactor(metafunc)
        calls_reactor = metafunc._calls  # noqa

        # detect union fixtures
        if is_fixture_union_params(argvalues):
            if ',' in argnames or not isinstance(argnames, string_types):
                raise ValueError("Union fixtures can not be parametrized")
            union_fixture_name = argnames
            union_fixture_alternatives = argvalues
            if indirect is False or len(kwargs) > 0:
                raise ValueError("indirect cannot be set on a union fixture, as well as unknown kwargs")

            # add a union parametrization in the queue (but do not apply it now)
            calls_reactor.append(UnionParamz(union_fixture_name, union_fixture_alternatives, ids, scope, kwargs))
        else:
            # add a normal parametrization in the queue (but do not apply it now)
            calls_reactor.append(NormalParamz(argnames, argvalues, indirect, ids, scope, kwargs))


class CallsReactor(object):
    """
    This object replaces the list of calls that was in `metafunc._calls`.
    It behaves like a list, but it actually builds that list dynamically based on all parametrizations collected
    from the custom `metafunc.parametrize` above.

    There are therefore three steps:

     - when `metafunc.parametrize` is called, this object gets called on `add_union` or `add_param`. A parametrization
     order gets stored in `self._pending`

     - when this object is first read as a list, all parametrization orders in `self._pending` are transformed into a
     tree in `self._tree`, and `self._pending` is discarded. This is done in `create_tree_from_pending_parametrization`.

     - finally, the list is built from the tree using `self._tree.to_call_list()`. This will also be the case in
     subsequent usages of this object.

    """
    __slots__ = 'metafunc', '_pending', '_call_list'

    def __init__(self, metafunc):
        self.metafunc = metafunc
        self._pending = []        # type: List[Union[UnionParamz, NormalParamz]]
        self._call_list = None

    # -- methods to provising parametrization orders without executing them --

    def append(self,
               parametrization  # type: Union[UnionParamz, NormalParamz]
               ):
        self._pending.append(parametrization)

    def print_parametrization_list(self):
        """Helper method to print all pending parametrizations in this reactor """
        print("\n".join([str(p) for p in self._pending]))

    # -- list facade --

    def __iter__(self):
        return iter(self.calls_list)

    def __getitem__(self, item):
        return self.calls_list[item]

    @property
    def calls_list(self):
        """
        Returns the list of calls. This property relies on self._tree, that is lazily created on first access,
        based on `self.parametrizations`.
        :return:
        """
        if self._call_list is None:
            # create the definitive tree.
            self.create_call_list_from_pending_parametrizations()

        return self._call_list

    # --- tree creation (executed once the first time this object is used as a list)

    def create_call_list_from_pending_parametrizations(self):
        """
        Takes all parametrization operations that are pending in `self._pending`,
        and creates a parametrization tree out of them.

        self._pending is set to None afterwards
        :return:
        """
        # self is on the _calls field, we'll temporarily remove it and finally set it back at the end of this call
        assert self.metafunc._calls is self

        # ------ parametrize the calls --------
        # create a dictionary of pending fixturenames/argnames to parametrize.
        pending_dct = OrderedDict()
        for p in self._pending:
            k = get_param_argnames_as_list(p[0])
            # remember one of the argnames only so that we are able to detect where in the fixture tree the
            # parametrization applies (it will still be applied for all of its argnames, no worries: see _process_node)
            k = k[0]
            pending_dct[k] = p

        if _DEBUG:
            print("\n---- pending parametrization ----")
            self.print_parametrization_list()
            print("---------------------------------\n")
            print("Applying all of them in the closure tree nodes:")

        # grab the "super fixtures closure" created previously (see getfixtureclosure above)
        super_closure = self.metafunc.fixturenames
        assert isinstance(super_closure, SuperClosure)

        # Apply parametrization for calls
        calls = get_calls_for_tree(self.metafunc, super_closure.tree, pending_dct)
        # Alternative: use the partitions for parametrization. The issue is that this leads to a less intuitive order
        # calls = []
        # for i in range(super_closure.nb_alternative_closures):
        #     calls += get_calls_for_partition(self.metafunc, super_closure, i, pending.copy())

        if _DEBUG:
            print("\n".join(["%s[%s]: funcargs=%s, params=%s" % (get_pytest_nodeid(self.metafunc),
                                                                 c.id, c.funcargs, c.params)
                             for c in calls]) + "\n")

        # clean EMPTY_ID set by @parametrize when there is at least a MultiParamsAlternative
        # if PYTEST54_OR_GREATER:
        for callspec in calls:
            remove_empty_ids(callspec)

        # save the list and put back self as the _calls facade
        self._call_list = calls
        self.metafunc._calls = self
        # forget about all parametrizations now - this wont happen again
        self._pending = None


def get_calls_for_tree(metafunc,
                       fix_closure_tree,  # type: FixtureClosureNode
                       pending_dct        # type: MutableMapping[str, Union[UnionParamz, NormalParamz]]
                       ):
    """
    Creates the list of calls for `metafunc` based on
    :param metafunc:
    :param fix_closure_tree:
    :param pending:
    :return:
    """
    pending_dct = pending_dct.copy()
    calls, nodes_used_by_calls = _process_node(metafunc, fix_closure_tree, pending_dct, [])
    # for each call in calls, the node in nodes_used_by_calls is the coresponding tree leaf.
    _cleanup_calls_list(metafunc, fix_closure_tree, calls, nodes_used_by_calls, pending_dct)
    return calls


def _cleanup_calls_list(metafunc,
                        fix_closure_tree,   # type: FixtureClosureNode
                        calls,              # type: List[CallSpec2]
                        nodes,              # type: List[FixtureClosureNode]
                        pending_dct         # type: MutableMapping[str, Union[UnionParamz, NormalParamz]]
                        ):
    """
    Cleans the calls list so that all calls contain a value for all parameters. This is basically
    about adding "NOT_USED" parametrization everywhere relevant.

    :param calls:
    :param nodes:
    :param pending:
    :return:
    """

    nb_calls = len(calls)
    if nb_calls != len(nodes):
        raise ValueError("This should not happen !")

    # create ref lists of fixtures per scope
    _not_always_used_func_scoped = []
    # _not_always_used_other_scoped = []
    for fixture_name in fix_closure_tree.get_not_always_used():
        try:
            fixdef = metafunc._arg2fixturedefs[fixture_name]  # noqa
        except KeyError:
            continue  # dont raise any error here and let pytest say "not found" later
        else:
            if has_function_scope(fixdef[-1]):
                _not_always_used_func_scoped.append(fixture_name)
            # else:
            #     _not_always_used_other_scoped.append(fixture_name)

    for i in range(nb_calls):
        c, n = calls[i], nodes[i]

        # A/ set to "not used" all parametrized fixtures that were not used in some branches
        for fixture, p_to_apply in pending_dct.items():
            if fixture not in c.params and fixture not in c.funcargs:
                # parametrize with a single "not used" value and discard the id
                if isinstance(p_to_apply, UnionParamz):
                    c_with_dummy = _parametrize_calls(metafunc, [c], p_to_apply.union_fixture_name, [NOT_USED],
                                                      indirect=True, discard_id=True, scope=p_to_apply.scope,
                                                      **p_to_apply.kwargs)
                else:
                    _nb_argnames = len(get_param_argnames_as_list(p_to_apply.argnames))
                    if _nb_argnames > 1:
                        _vals = [(NOT_USED,) * _nb_argnames]
                    else:
                        _vals = [NOT_USED]
                    c_with_dummy = _parametrize_calls(metafunc, [c], p_to_apply.argnames, _vals,
                                                      indirect=p_to_apply.indirect, discard_id=True,
                                                      scope=p_to_apply.scope, **p_to_apply.kwargs)
                assert len(c_with_dummy) == 1
                calls[i] = c_with_dummy[0]
                c = calls[i]

        # B/ function-scoped non-parametrized fixtures also need to be explicitly deactivated in the callspecs
        # where they are not required, otherwise they will be setup/teardown.
        #
        # For this we use a dirty hack: we add a parameter with they name in the callspec, it seems to be propagated
        # in the `request`. TODO is there a better way?
        for fixture_name in _not_always_used_func_scoped:
            if fixture_name not in c.params and fixture_name not in c.funcargs:
                if not n.requires(fixture_name):
                    # explicitly add it as discarded by creating a parameter value for it.
                    c.params[fixture_name] = NOT_USED
                    c.indices[fixture_name] = 1
                    set_callspec_arg_scope_to_function(c, fixture_name)
                else:
                    # explicitly add it as active
                    c.params[fixture_name] = USED
                    c.indices[fixture_name] = 0
                    set_callspec_arg_scope_to_function(c, fixture_name)

    # finally, if there are some session or module-scoped fixtures that
    # are used in *none* of the calls, they could be deactivated too
    # (see https://github.com/smarie/python-pytest-cases/issues/137)
    #
    # for fixture_name in _not_always_used_other_scoped:
    #     _scopenum = metafunc._arg2fixturedefs[fixture_name][-1].scopenum
    #
    #     # check if there is at least one call that actually uses the fixture and is not skipped...
    #     # this seems a bit "too much" !! > WONT FIX
    #     used = False
    #     for i in range(nb_calls):
    #         c, n = calls[i], nodes[i]
    #         if fixture_name in c.params or fixture_name in c.funcargs or n.requires(fixture_name):
    #             if not is_skipped_or_failed(c):  # HOW can we implement this based on call (and not item) ???
    #                 used = True
    #                 break
    #
    #     if not used:
    #         # explicitly add it as discarded everywhere by creating a parameter value for it.
    #         for i in range(nb_calls):
    #             c = calls[i]
    #             c.params[fixture_name] = NOT_USED
    #             c.indices[fixture_name] = 0
    #             c._arg2scopenum[fixture_name] = _scopenum  # noqa


# def get_calls_for_partition(metafunc, super_closure, p_idx, pending):
#     """
#     Parametrizes all fixtures that are actually used in this partition
#     Cleans the calls list so that all calls contain a value for all parameters. This is basically
#     about adding "NOT_USED" parametrization everywhere relevant.
#
#     :return: a list of CallSpec2
#     """
#     calls = []
#
#     # A/ parametrize all fixtures that are actually used in this partition
#     for fixture_name in super_closure.partitions[p_idx]:
#         try:
#             # pop it from pending - do not rely the order in pending but rather the order in the closure
#             p_to_apply = pending.pop(fixture_name)
#         except KeyError:
#             # not a parametrized fixture
#             continue
#         else:
#             if isinstance(p_to_apply, UnionParamz):
#                 # ******** Union parametrization **********
#                 # selected_ids, selected_alternative = super_closure.get_parameter_to_apply(p_to_apply, p_idx)
#                 num, selected_filter = super_closure.filters[p_idx][p_to_apply.union_fixture_name]
#                 # in order to get the *actual* id to use (with all pytest subtleties in case of two identical ids
#                 # appearing in the list), we create a fake calls list
#                 fake_calls = _parametrize_calls(metafunc, [], p_to_apply.union_fixture_name,
#                                                 p_to_apply.alternative_names, ids=p_to_apply.ids,
#                                                 scope=p_to_apply.scope, indirect=True, **p_to_apply.kwargs)
#                 selected_id = fake_calls[num].id
#                 selected_alternative = p_to_apply.alternative_names[num]
#                 # assert selected_alternative.alternative_name == selected_filter
#
#                 if _DEBUG:
#                     print("[Partition %s] Applying parametrization for UNION fixture %r=%r"
#                           "" % (p_idx, p_to_apply.union_fixture_name, selected_alternative))
#
#                 # always use 'indirect' since that's a fixture.
#                 calls = _parametrize_calls(metafunc, calls, p_to_apply.union_fixture_name,
#                                            [selected_alternative], ids=[selected_id], scope=p_to_apply.scope,
#                                            indirect=True, **p_to_apply.kwargs)
#
#             elif isinstance(p_to_apply, NormalParamz):
#                 # ******** Normal parametrization **********
#                 if _DEBUG:
#                     print("[Partition %s] Applying parametrization for NORMAL %s"
#                           "" % (p_idx, p_to_apply.argnames))
#
#                 calls = _parametrize_calls(metafunc, calls, p_to_apply.argnames, p_to_apply.argvalues,
#                                            indirect=p_to_apply.indirect, ids=p_to_apply.ids,
#                                            scope=p_to_apply.scope, **p_to_apply.kwargs)
#             else:
#                 raise TypeError("Invalid parametrization type: %s" % p_to_apply.__class__)
#
#     # Cleaning
#     for i in range(len(calls)):
#         c = calls[i]
#
#         # B/ set to "not used" all parametrized fixtures that were not used in some branches
#         for fixture_name, p_to_apply in pending.items():
#             if fixture_name not in c.params and fixture_name not in c.funcargs:
#                 # parametrize with a single "not used" value and discard the id
#                 if isinstance(p_to_apply, UnionParamz):
#                     c_with_dummy = _parametrize_calls(metafunc, [c], p_to_apply.union_fixture_name, [NOT_USED],
#                                                       indirect=True, discard_id=True, scope=p_to_apply.scope,
#                                                       **p_to_apply.kwargs)
#                 else:
#                     _nb_argnames = len(get_param_argnames_as_list(p_to_apply.argnames))
#                     if _nb_argnames > 1:
#                         _vals = [(NOT_USED,) * _nb_argnames]
#                     else:
#                         _vals = [NOT_USED]
#                     c_with_dummy = _parametrize_calls(metafunc, [c], p_to_apply.argnames, _vals,
#                                                       indirect=p_to_apply.indirect, discard_id=True,
#                                                       scope=p_to_apply.scope, **p_to_apply.kwargs)
#                 assert len(c_with_dummy) == 1
#                 calls[i] = c_with_dummy[0]
#                 c = calls[i]
#
#         # C/ some non-parametrized fixtures may also need to be explicitly deactivated in some callspecs
#         # otherwise they will be setup/teardown.
#         #
#         # For this we use a dirty hack: we add a parameter with they name in the callspec, it seems to be propagated
#         # in the `request`. TODO is there a better way?
#         for fixture_name in super_closure.get_not_always_used():
#             try:
#                 fixdef = metafunc._arg2fixturedefs[fixture_name]  # noqa
#             except KeyError:
#                 continue  # dont raise any error here and instead let pytest say "not found"
#
#             if fixture_name not in c.params and fixture_name not in c.funcargs:
#                 if not super_closure.requires(fixture_name, p_idx):
#                     # explicitly add it as discarded by creating a parameter value for it.
#                     c.params[fixture_name] = NOT_USED
#                     c.indices[fixture_name] = 1
#                     c._arg2scopenum[fixture_name] = get_pytest_scopenum(fixdef[-1].scope)  # noqa
#                 else:
#                     # explicitly add it as active by creating a parameter value for it.
#                     c.params[fixture_name] = 'used'
#                     c.indices[fixture_name] = 0
#                     c._arg2scopenum[fixture_name] = get_pytest_scopenum(fixdef[-1].scope)  # noqa
#
#     return calls


@property
def id(self):
    # legacy _CallSpec2 id was filtering empty strings, we'll put it back on the class below
    # https://github.com/pytest-dev/pytest/blob/5.3.4/src/_pytest/python.py#L861
    return "-".join(map(str, filter(None, self._idlist)))


def _parametrize_calls(metafunc, init_calls, argnames, argvalues, discard_id=False, indirect=False, ids=None,
                       scope=None, **kwargs):
    """Parametrizes the initial `calls` with the provided information and returns the resulting new calls"""

    # make a backup so that we can restore the metafunc at the end
    bak = metafunc._calls  # noqa

    # place the initial calls on the metafunc
    metafunc._calls = init_calls if init_calls is not None else []

    # parametrize the metafunc. Since we replaced the `parametrize` method on `metafunc` we have to call super
    metafunc.__class__.parametrize(metafunc, argnames, argvalues, indirect=indirect, ids=ids, scope=scope, **kwargs)

    # extract the result
    new_calls = metafunc._calls  # noqa

    # If the user wants to discard the newly created id, remove the last id in all these callspecs in this node
    if discard_id:
        for callspec in new_calls:
            callspec._idlist.pop(-1)  # noqa

    # restore the metafunc and return the new calls
    metafunc._calls = bak
    return new_calls


def _process_node(metafunc,
                  current_node,  # type: FixtureClosureNode
                  pending,       # type: MutableMapping[str, Union[UnionParamz, NormalParamz]]
                  calls          # type: List[CallSpec2]
                  ):
    """
    Routine to apply all the parametrization tasks in `pending` that are relevant to `current_node`,
    to `calls` (a list of pytest CallSpec2).

    It first applies all parametrization that correspond to current node (normal parameters),
    then applies the "split" parametrization if needed and recurses into each tree branch.

    It returns a tuple containing a list of calls and a list of same length containing which leaf node each one
    corresponds to.

    :param metafunc:
    :param current_node: the closure tree node we're focusing on
    :param pending: a list of parametrization orders to apply
    :param calls:
    :return: a tuple (calls, nodes) of two lists of the same length. So that for each CallSpec calls[i], you can see
        the corresponding leaf node in nodes[i]
    """

    # (1) first apply all **non-split** fixtures at this node = NORMAL PARAMETERS
    # in the order defined in the closure tree, do not trust the order of the received parametrize (`pending`)
    fixtures_at_this_node = [f for f in current_node.fixture_defs.keys()
                             if f is not current_node.split_fixture_name]
    for fixturename in fixtures_at_this_node:
        try:
            # pop the corresponding parametrization from pending - do not trust the order
            p_to_apply = pending.pop(fixturename)
        except KeyError:
            # fixturename is not a parametrized fixture, nothing to do
            continue
        else:
            if isinstance(p_to_apply, UnionParamz):
                raise ValueError("This should not happen! Only Normal parameters should be in fixtures_at_this_node")
            elif isinstance(p_to_apply, NormalParamz):
                # ******** Normal parametrization **********
                if _DEBUG:
                    print("[Node %s] Applying parametrization for NORMAL %s"
                          "" % (current_node.to_str(with_children=False), p_to_apply.argnames))

                calls = _parametrize_calls(metafunc, calls, p_to_apply.argnames, p_to_apply.argvalues,
                                           indirect=p_to_apply.indirect, ids=p_to_apply.ids,
                                           scope=p_to_apply.scope, **p_to_apply.kwargs)
            else:
                raise TypeError("Invalid parametrization type: %s" % p_to_apply.__class__)

    # (2) then is there a "union" = a split between two sub-branches in the tree ?
    if not current_node.has_split():
        # No split = tree leaf: return
        nodes = [current_node] * len(calls)
        return calls, nodes
    else:
        # There is a **split** : apply its parametrization (a UNION parameter)
        try:
            # pop the corresponding parametrization from pending - do not trust the order
            p_to_apply = pending.pop(current_node.split_fixture_name)
        except KeyError:
            raise ValueError("This should not happen! fixture union parametrization missing, but this is a split node")
        else:
            if isinstance(p_to_apply, NormalParamz):
                raise ValueError("This should not happen! Split nodes correspond to Union parameters, not Normal ones.")
            elif isinstance(p_to_apply, UnionParamz):
                # ******** Union parametrization **********
                if _DEBUG:
                    print("[Node %s] Applying parametrization for UNION %s"
                          "" % (current_node.to_str(with_children=False), p_to_apply.union_fixture_name))

                # always use 'indirect' since that's a fixture.
                calls = _parametrize_calls(metafunc, calls, p_to_apply.union_fixture_name,
                                           p_to_apply.alternative_names, indirect=True,
                                           ids=p_to_apply.ids, scope=p_to_apply.scope, **p_to_apply.kwargs)

                # now move to the children
                nodes_children = [None] * len(calls)
                for i in range(len(calls)):
                    active_alternative = calls[i].params[p_to_apply.union_fixture_name]
                    child_indices = [_i for _i, x in enumerate(current_node.split_fixture_alternatives)
                                     if x == active_alternative.alternative_name]
                    # only use the first matching child, since the subtrees are identical.
                    child_node = current_node.children[child_indices[0]]
                    child_pending = pending.copy()

                    # place the childs parameter in the first position if it is in the list
                    # not needed anymore - already automatic
                    # try:
                    #     child_pending.move_to_end(child_alternative, last=False)
                    # except KeyError:
                    #     # not in the list: the child alternative is a non-parametrized fixture
                    #     pass

                    calls[i], nodes_children[i] = _process_node(metafunc, child_node, child_pending, [calls[i]])

                # finally flatten the list if needed
                calls = flatten_list(calls)
                nodes_children = flatten_list(nodes_children)
                return calls, nodes_children


# def _make_unique(lst):
#     _set = set()
#
#     def _first_time_met(v):
#         if v not in _set:
#             _set.add(v)
#             return True
#         else:
#             return False
#
#     return [v for v in lst if _first_time_met(v)]


def flatten_list(lst):
    return [v for nested_list in lst for v in nested_list]


def sort_according_to_ref_list(fixturenames, param_names):
    """
    Sorts items in the first list, according to their position in the second.
    Items that are not in the second list stay in the same position, the others are just swapped.
    A new list is returned.

    :param fixturenames:
    :param param_names:
    :return:
    """
    cur_indices = []
    for pname in param_names:
        try:
            cur_indices.append(fixturenames.index(pname))
        except (ValueError, IndexError):
            # can happen in case of indirect parametrization: a parameter is not in the fixture name.
            # TODO we should maybe rather add the pname to fixturenames in this case ?
            pass
    target_indices = sorted(cur_indices)
    sorted_fixturenames = list(fixturenames)
    for old_i, new_i in zip(cur_indices, target_indices):
        sorted_fixturenames[new_i] = fixturenames[old_i]
    return sorted_fixturenames


_OPTION_NAME = 'with_reorder'
_SKIP = 'skip'
_NORMAL = 'normal'
_OPTIONS = {
    _NORMAL: """(default) the usual reordering done by pytest to optimize setup/teardown of session- / module-
/ class- fixtures, as well as all the modifications made by other plugins (e.g. pytest-reorder)""",
    _SKIP: """skips *all* reordering, even the one done by pytest itself or installed plugins
(e.g. pytest-reorder)"""
}


# @hookspec(historic=True)
def pytest_addoption(parser):
    group = parser.getgroup('pytest-cases ordering', 'pytest-cases reordering options', after='general')
    help_str = """String specifying one of the reordering alternatives to use. Should be one of :
 - %s""" % ("\n - ".join(["%s: %s" % (k, v) for k, v in _OPTIONS.items()]))
    group.addoption(
        '--%s' % _OPTION_NAME.replace('_', '-'), type=str, default='normal', help=help_str
    )


# will be loaded when the pytest_configure hook below is called
PYTEST_CONFIG = None  # type: Optional[Config]


def pytest_load_initial_conftests(early_config):
    # store the received config object for future use; see #165 #166 #196
    global PYTEST_CONFIG
    PYTEST_CONFIG = early_config


# @hookspec(historic=True)
def pytest_configure(config):
    # validate the config
    allowed_values = ('normal', 'skip')
    reordering_choice = config.getoption(_OPTION_NAME)
    if reordering_choice not in allowed_values:
        raise ValueError("[pytest-cases] Wrong --%s option: %s. Allowed values: %s"
                         "" % (_OPTION_NAME, reordering_choice, allowed_values))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):  # noqa
    """
    An alternative to the `reorder_items` function in fixtures.py
    (https://github.com/pytest-dev/pytest/blob/master/src/_pytest/fixtures.py#L209)

    We basically set back the previous order once the pytest ordering routine has completed.

    TODO we should set back an optimal ordering, but current PR https://github.com/pytest-dev/pytest/pull/3551
     will probably not be relevant to handle our "union" fixtures > need to integrate the NOT_USED markers in the method

    :param session:
    :param config:
    :param items:
    :return:
    """
    ordering_choice = config.getoption(_OPTION_NAME)

    if ordering_choice == _SKIP:
        # remember initial order
        initial_order = copy(items)
        yield
        # put back the initial order but keep the filter
        to_return = [None] * len(items)
        i = 0
        for item in initial_order:
            if item in items:
                to_return[i] = item
                i += 1
        assert i == len(items)
        items[:] = to_return

    else:
        # do nothing
        yield


@pytest.fixture
def current_cases(request):
    """
    A fixture containing `get_current_cases(request)`

    This is a dictionary containing all case parameters for the currently active `pytest` item.
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
    """
    return get_current_cases(request)
