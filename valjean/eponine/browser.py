'''Module to access in easy way results stored in list of dictionaries.

This module is composed of 2 classes:

  * :class:`Browser` that stores the list of dictionaries and builds an
    :class:`Index` to facilitate selections;
  * :class:`Index` based on :class:`collections.defaultdict` to perform
    selections on the list of dictionaries


The classes :class:`Index` and :class:`Browser` are meant to be general even if
they will be shown and used in a specific case: parsing results from Tripoli-4.


The :class:`Index` class
------------------------

This class is based on an inheritance from :class:`collections.abc.Mapping`
from :mod:`collections`. It implements a ``defaultdict(defaultdict(set))`` from
:class:`collections.defaultdict`.

:class:`set` contains `int` that corresponds to the index of the dictionary in
the list of dictionaries.

:class:`Index` is not supposed to be used standalone, but called from
:class:`Browser`, but this is still possible.


The :class:`Browser` class
--------------------------

This class is analogue to a phonebook: it contains an index and the content,
here stored as a list of dictionaries. It commands the index (building and
selections). Examples are shown below.


.. _browser-example:

Building the browser
^^^^^^^^^^^^^^^^^^^^

Let's consider a bunch of friends going to the restaurant and ordering their
menus. For each of them the waiter has to remember their name, under
``'consumer'``, their choice of menu under ``'menu'``, their drink, what they
precisely order as dish under ``'results'`` and optionally the number
corresponding to their choice of dessert. He will represent these orders as a
list of orders, one order being a dictionary.

>>> from valjean.eponine.browser import Browser
>>> from pprint import pprint
>>> orders = [
... {'menu': '1', 'consumer': 'Terry', 'drink': 'beer',
...  'results': {'ingredients_res': ['egg', 'bacon']}},
... {'menu': '2', 'consumer': 'John',
...  'results': [{'ingredients_res': ['egg', 'spam']},
...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
... {'menu': '1', 'consumer': 'Graham', 'drink': 'coffee',
...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
... {'menu': '3', 'consumer': 'Eric', 'drink': 'beer',
...  'results': {'ingredients_res': ['sausage'],
...              'side_res': 'baked beans'}},
... {'menu': 'royal', 'consumer': 'Michael', 'drink': 'brandy', 'dessert': 3,
...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
>>> com_br = Browser(orders)
>>> print(com_br)
Browser object -> Number of content items: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'index', 'menu']
               -> Number of globals: 0

Some global variables can be added, as a dictionary, normally common to all the
results sent under the argument ``content``.

>>> global_vars = {'table': 42, 'service_time': 300, 'priority': -1}
>>> com_br = Browser(orders, global_vars=global_vars)
>>> print(com_br)
Browser object -> Number of content items: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'index', 'menu']
               -> Number of globals: 3
>>> pprint(com_br.globals)
{'priority': -1, 'service_time': 300, 'table': 42}


Selection of a given items or of a list of items from content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Various methods are available to select one order, depending on requirements:

  * get a new Browser:

    >>> sel_br = com_br.filter_by(menu='1', drink='beer')
    >>> pprint(sel_br.content)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Terry',  'drink': 'beer', 'index': 0, 'menu': '1', \
'results': {'ingredients_res': ['egg', 'bacon']}}]

    * check if a key is present or not:

    >>> 'drink' in sel_br
    True
    >>> 'dessert' in sel_br
    False
    >>> 'dessert' in com_br
    True

    The ``'dessert'`` key has been removed from the Browser issued from
    the selection while it is still present in the original one.

  * get the available keys (sorted to be able to test them in the doctest, else
    list is enough):

    >>> sorted(sel_br.keys())
    ['consumer', 'drink', 'index', 'menu']
    >>> sorted(com_br.keys())
    ['consumer', 'dessert', 'drink', 'index', 'menu']

  * if the required key doesn't exist a warning is emitted:

    >>> sel_br = com_br.filter_by(quantity=5)
    >>> # prints  WARNING     browser: quantity not a valid key. Possible \
ones are ['consumer', 'dessert', 'drink', 'index', 'menu']
    >>> 'quantity' in com_br
    False

  * if the value corresponding to the key doesn't exist another warning is
    emitted:

    >>> sel_br = com_br.filter_by(drink='wine')
    >>> # prints  WARNING     browser: wine is not a valid drink

  * to know the available values corresponding to the keys (without the
    corresponding items indexes):

    >>> sorted(com_br.available_values('drink'))
    ['beer', 'brandy', 'coffee']

  * if the key doesn't exist an 'empty generator' is emitted:

    >>> sorted(com_br.available_values('quantity'))
    []

  * to directly get the content items corresponding to the selection, use the
    method :func:`Browser.select_by`

    >>> sel_br = com_br.select_by(consumer='Graham')
    >>> type(sel_br)
    <class 'list'>
    >>> len(sel_br)
    1
    >>> pprint(sel_br)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Graham', 'drink': 'coffee', 'index': 2, 'menu': '1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}]

  * this also work when several items correspond to the selection:

    >>> sel_br = com_br.select_by(drink='beer')
    >>> pprint(sel_br)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Terry', 'drink': 'beer', 'index': 0, 'menu': '1', \
'results': {'ingredients_res': ['egg', 'bacon']}}, \
{'consumer': 'Eric', 'drink': 'beer', 'index': 3, 'menu': '3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}}]
    >>> len(sel_br)
    2

  * a *squeeze* option is also available to directly get the item (and not a
    list of items) when **only one** item corresponds to the selection (its
    default is at False):

    >>> item = com_br.select_by(consumer='Graham', squeeze=True)
    >>> pprint(item)  # doctest: +NORMALIZE_WHITESPACE
    {'consumer': 'Graham', 'drink': 'coffee', 'index': 2, 'menu': '1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}

  * squeeze is not possible if several results correspond to the required
    selection

    >>> items = com_br.select_by(drink='beer', squeeze=True)
    >>> # prints  WARNING     browser: Squeeze cannot be applied, more than \
one content item corresponds to your choice


Module API
----------
'''

import logging
from collections import defaultdict
from collections.abc import Mapping, Container


LOGGER = logging.getLogger('valjean')


def _make_defaultdict_set():
    '''The sole purpose of this function is to give a name to the defaultdict
    factory in :meth:`Index.index`. Without a name, the :class:`Index` class
    cannot be serialized by :mod:`pickle`.
    '''
    return defaultdict(set)


class Index(Mapping):
    '''Class to describe index used in Browser.

    The structure of Index is a ``defaultdict(defaultdict(set))``.  This class
    was derived mainly for pretty-printing purposes.

    Quick example of index (menu for 4 persons, identified by numbers, one has
    no drink):

    >>> from valjean.eponine.browser import Index
    >>> myindex = Index()
    >>> myindex.index['drink']['beer'] = {1, 4}
    >>> myindex.index['drink']['wine'] = {2}
    >>> myindex.index['menu']['spam'] = {1, 3}
    >>> myindex.index['menu']['egg'] = {2}
    >>> myindex.index['menu']['bacon'] = {4}
    >>> myindex.dump(sort=True)
    "{'drink': {'beer': {1, 4}, 'wine': {2}}, \
'menu': {'bacon': {4}, 'egg': {2}, 'spam': {1, 3}}}"
    >>> 'drink' in myindex
    True
    >>> 'consumer' in myindex
    False
    >>> len(myindex)
    2
    >>> for k in sorted(myindex):
    ...    print(k, sorted(myindex[k].keys()))
    drink ['beer', 'wine']
    menu ['bacon', 'egg', 'spam']

    The :func:`keep_only` method allows to get a sub-Index from a given set of
    ids (int), removing all keys not involved in the corresponding ids:

    >>> myindex.keep_only({2}).dump(sort=True)
    "{'drink': {'wine': {2}}, 'menu': {'egg': {2}}}"
    >>> menu_clients14 = myindex.keep_only({1, 4})
    >>> sorted(menu_clients14.keys()) == ['drink', 'menu']
    True
    >>> list(menu_clients14['drink'].keys()) == ['beer']
    True
    >>> list(menu_clients14['drink'].values()) == [{1, 4}]
    True
    >>> sorted(menu_clients14['menu'].keys()) == ['bacon', 'spam']
    True
    >>> menu_clients14['menu']['spam'] == {1}
    True
    >>> 3 in menu_clients14['menu']['spam']
    False
    >>> menu_client3 = myindex.keep_only({3})
    >>> list(menu_client3.keys()) == ['menu']
    True
    >>> 'drink' in menu_client3
    False

    The key ``'drink'`` has been removed from the last index as 2 did not
    required it.

    If you print an :class:`Index`, it looks like a standard dictionary (``{
    ... }`` instead of ``defaultdict(...)``) but the keys are not sorted:

    >>> print(myindex)
    {...: {...: {...}...}}
    '''

    def __init__(self):
        self.index = defaultdict(_make_defaultdict_set)

    def __str__(self):
        lstr = ["{"]
        for i, (key, dset) in enumerate(list(self.index.items())):
            lstr.append('{0!r}: {{'.format(key))
            for j, (dkey, ind) in enumerate(list(dset.items())):
                lstr.append('{0!r}: {1!r}'.format(dkey, ind))
                if j < len(dset) - 1:
                    lstr.append(', ')
            lstr.append('}')
            if i < len(self.index) - 1:
                lstr.append(', ')
        lstr.append('}')
        return ''.join(lstr)

    def __repr__(self):
        return self.index.__repr__()

    def __getitem__(self, item):
        return self.index.__getitem__(item)

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def __contains__(self, key):
        return self.index.__contains__(key)

    def keep_only(self, ids):
        '''Get an :class:`Index` containing only the relevant keywords for the
        required set of ids.

        :param set(int) ids: index corresponding to the required elements of
          the list of content items
        :returns: Index only containing the keys involved in the ids
        '''
        assert isinstance(ids, set)
        lind = Index()
        if not ids:
            return lind
        for key in self.index:
            for kwd, kset in self.index[key].items():
                tmpset = kset & ids
                if tmpset:
                    lind[key][kwd] = tmpset
        return lind

    def dump(self, *, sort=False):
        '''Dump the Index.

        If ``sort == False`` (default case), returns :func:`__str__` result,
        else returns sorted Index (alphabetic order for keys).
        '''
        if sort:
            lstr = ["{"]
            for i, (key, dset) in enumerate(sorted(self.index.items())):
                lstr.append('{0!r}: {{'.format(key))
                for j, (dkey, ind) in enumerate(sorted(dset.items(), key=str)):
                    lstr.append('{0!r}: {1!r}'.format(dkey, ind))
                    if j < len(dset) - 1:
                        lstr.append(', ')
                lstr.append('}')
                if i < len(self.index) - 1:
                    lstr.append(', ')
            lstr.append('}')
            return ''.join(lstr)
        return str(self)


class Browser(Container):
    '''Class to perform selections on results.

    This class is based on four objects:

      * the content, as a list of dictionaries (containing data and metadata)
      * the key corresponding to data in the dictionary (default='results')
      * an index based on content elements allowing easy selections on each
        metadata
      * a dictionary corresponding to global variables (common to all content
        items).

    Initialization parameters:

    :param list(dict) content: list of items containing data and metadata
    :param str data_key: key in the content items corresponding to results or
      data, that should not be used in index (as always present and mandatory)
    :param dict global_vars: global variables (optional, default=None)

    An additional key is added at the Index construction: ``'index'`` in order
    to keep track of the order of the list and being able to do selection on
    it.

    Examples on development / debugging methods:

    Let's use the example detailled above in
    :ref:`module introduction <browser-example>`:

    >>> from valjean.eponine.browser import Browser
    >>> orders = [
    ... {'menu': '1', 'consumer': 'Terry', 'drink': 'beer',
    ...  'results': {'ingredients_res': ['egg', 'bacon']}},
    ... {'menu': '2', 'consumer': 'John',
    ...  'results': [{'ingredients_res': ['egg', 'spam']},
    ...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
    ... {'menu': '1', 'consumer': 'Graham', 'drink': 'coffee',
    ...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
    ... {'menu': '3', 'consumer': 'Eric', 'drink': 'beer',
    ...  'results': {'ingredients_res': ['sausage'],
    ...              'side_res': 'baked beans'}},
    ... {'menu': 'royal', 'consumer': 'Michael', 'drink': 'brandy',
    ...  'dessert': 3,
    ...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
    >>> com_br = Browser(orders)

    * possibility to get the item id directly (internally used method):

      >>> ind = com_br._filter_items_id_by(drink='coffee')
      >>> isinstance(ind, set)
      True
      >>> print(ind)
      {2}

    * possibility to get the index of the content element stripped without
      rebuilding the full Browser:

      >>> ind = com_br._filter_index_by(menu='1')
      >>> isinstance(ind, Index)
      True
      >>> ind.dump(sort=True)  # doctest: +NORMALIZE_WHITESPACE
      "{'consumer': {'Graham': {2}, 'Terry': {0}}, \
'drink': {'beer': {0}, 'coffee': {2}}, 'index': {0: {0}, 2: {2}}, \
'menu': {'1': {0, 2}}}"

      The 'dessert' key has been stripped from the index:

      >>> 'dessert' in ind
      False

    Debug print is available thanks to :func:`__repr__`:

    >>> small_order = [{'dessert': 1, 'drink': 'beer', 'results': ['spam']}]
    >>> so_br = Browser(small_order)
    >>> "{0!r}".format(so_br)
    "<class 'valjean.eponine.browser.Browser'>, (Content items: ..., \
Index: ...)"
    '''

    def __init__(self, content, data_key='results', global_vars=None):
        self.content = [r.copy() for r in content]
        self.data_key = data_key
        self.index = self._build_index()
        LOGGER.debug("Index: %s", self.index)
        self.globals = (global_vars.copy() if isinstance(global_vars, dict)
                        else {})

    def __eq__(self, other):
        return (self.content == other.content
                and self.data_key == other.data_key
                and self.globals == other.globals)

    def __ne__(self, other):
        return not self == other

    def _build_index(self):
        '''Build index from all content elements in the list.

        Keys of the sets are keywords used to describe the items and/or the
        scores (if flat case).

        :param str data_key: key in list of content items corresponding to
          results or data
        :returns: :class:`Index`
        '''
        index = Index()
        for ielt, elt in enumerate(self.content):
            elt['index'] = ielt
            for key in elt:
                if key != self.data_key:
                    index[key][elt[key]].add(ielt)
        return index

    def __contains__(self, key):
        if key in self.index:
            return True
        return False

    def __len__(self):
        return len(self.content)

    def is_empty(self):
        '''Check if the Browser is empty or not.

        Empty meaning no elements in content AND no globals.
        '''
        return not self.content and not self.globals

    def merge(self, other):
        '''Merge two browsers.

        This method merge 2 browsers: the *other* one appears then at the
        end of the *self* one. Global variables are also merged. The new index
        correspond to the merged case.

        :param Browser other: another browser
        :rtype: Browser
        '''
        if self.data_key != other.data_key:
            raise ValueError('Same data_key is required to merge Browsers')
        if self.globals != other.globals:
            LOGGER.info('globals will be updated with other values')
        new_glob = self.globals.copy()
        new_glob.update(other.globals)
        new_content = self.content + other.content
        LOGGER.debug("Nb self items (%d) + Nb other items (%d) = %d",
                     len(self), len(other), len(new_content))
        return Browser(new_content, data_key=self.data_key,
                       global_vars=new_glob)

    def keys(self):
        '''Get the available keys in the index (so in the items list). As
        usual it returns a generator.
        '''
        return self.index.keys()

    def available_values(self, key):
        '''Get the available keys in the *second* level, i.e. under the given
        external one.

        :param str key: 'external' key (from outer defaultdict)
        :returns: generator with corresponding keys (or empty one)
        '''
        if key in self:
            yield from self.index[key].keys()
        else:
            yield from ()

    def __str__(self):
        return ("{0} object -> Number of content items: {1}, "
                "data key: {2!r}, available metadata keys: {3}\n"
                "{4:>{5}}        -> Number of globals: {6}"
                .format(self.__class__.__name__, len(self.content),
                        self.data_key, sorted(self.keys()), "",
                        len(self.__class__.__name__), len(self.globals)))

    def __repr__(self):
        return ("{0}, (Content items: {1!r}, Index: {2!r})"
                .format(self.__class__, self.content, self.index))

    def _filter_items_id_by(self, **kwargs):
        '''Selection of content items indices according to kwargs criteria.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :return: set of ids
        :rtype: set(int)
        '''
        itemids = set(range(len(self.content)))
        for kwd in kwargs:
            if kwd not in self.index:
                LOGGER.warning("%s not a valid key. Possible ones are %s",
                               kwd, sorted(self.keys()))
                return set()
            if kwargs[kwd] not in self.index[kwd]:
                LOGGER.warning("%s is not a valid %s", kwargs[kwd], kwd)
                return set()
            itemids = itemids & self.index[kwd][kwargs[kwd]]
        if not itemids:
            LOGGER.warning("Wrong selection, item might be not present. "
                           "Also check if requirements are consistent.")
            return set()
        return itemids

    def _filter_index_by(self, **kwargs):
        '''Get index corresponding to selection given thanks to keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required item.
            More than one are allowed.
        :returns: :class:`Index` (stripped from useless keys)
        '''
        itemids = self._filter_items_id_by(**kwargs)
        return self.index.keep_only(itemids)

    def filter_by(self, include=(), exclude=(), **kwargs):
        '''Get a Browser corresponding to selection from keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required item.
            More than one are allowed.
        :param tuple(str) include: metadata keys required in the content items
            but for which the value is not necessarly known
        :param tuple(str) exclude: metadata that should not be present in the
            items and for which the value is not necessarly known
        :returns: :class:`Browser` (subset of the default one, corresponding to
            the selection)
        '''
        LOGGER.debug("in select_by, kwargs=%s", kwargs)
        sincl, sexcl = set(include), set(exclude)
        respids = self._filter_items_id_by(**kwargs)
        lresp = [self.content[i] for i in sorted(respids)
                 if sincl.issubset(self.content[i])
                 and not sexcl.intersection(self.content[i])]
        sub_br = Browser(lresp, global_vars=self.globals)
        return sub_br

    def select_by(self, *, squeeze=False, include=(), exclude=(), **kwargs):
        '''Get an item or the list of items from content corresponding to
        selection from keyword arguments.

        :param \\**\\kwargs: keyword arguments to specify the required items.
            More than one are allowed.
        :param bool squeeze: named parameter
        :param tuple(str) include: metadata keys required in the items but for
            which the value is not necessarly known
        :param tuple(str) exclude: metadata that should not be present in the
          items and for which the value is not necessarly known
        :returns: first element of the list of content items if only one,
          else list of content items matching the requirements
        '''
        respids = self._filter_items_id_by(**kwargs)
        sincl, sexcl = set(include), set(exclude)
        litems = [self.content[i] for i in sorted(respids)
                  if sincl.issubset(self.content[i])
                  and not sexcl.intersection(self.content[i])]
        if squeeze:
            if not litems:
                LOGGER.warning("No item corresponding to the selection.")
                return None
            if len(litems) > 1:
                LOGGER.warning("Squeeze cannot be applied, several content "
                               "items correspond to your choice")
                return None
            return litems[0]
        return litems
