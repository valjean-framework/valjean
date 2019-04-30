'''
Module to access Tripoli-4 parsed results.

  * :class:`Accessor` that allows to access and select in easier way the
    various elements of the parsing results, using internally the 2 follwing
    classes;


Description of :class:`Accessor`
--------------------------------

The :class:`Accessor` class is the real access point to the list of responses
but not only. The result from parsing is its default input. This parsing result
is necessarly a dictionary, i.e. if you get a list of dictionary because you
required to parse more than one batch you'll need to access them thanks to a
loop over the list of batches. Accessor also allows simplified access to other
data like simulation time or number of batch.

For example, let's consider a parsing results that contains the same ``orders``
as in :mod:`.response_book`, represented as a list of dictionaries. It will be
stored under the key ``'list_responses'`` and additional items will be added to
that dictionary for it to look like a default parsing results one.

>>> from valjean.eponine.tripoli4.accessor import Accessor
>>> from pprint import pprint
>>> orders = [
... {'response_function': 'menu1', 'consumer': 'Terry', 'drink': 'beer',
...  'results': {'ingredients_res': ['egg', 'bacon']}},
... {'response_function': 'menu2', 'consumer': 'John',
...  'results': [{'ingredients_res': ['egg', 'spam']},
...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
... {'response_function': 'menu1', 'consumer': 'Graham', 'drink': 'coffee',
...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
... {'response_function': 'menu3', 'consumer': 'Eric', 'drink': 'beer',
...  'results': {'ingredients_res': ['sausage'],
...              'side_res': 'baked beans'}},
... {'response_function': 'royal_menu', 'consumer': 'Michael',
...  'drink': 'brandy', 'dessert': 3,
...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
>>> pres = {'edition_batch_number': 42, 'list_responses': orders,
...         'service_time': 300}
>>> pprint(pres)  # doctest: +NORMALIZE_WHITESPACE
{'edition_batch_number': 42, 'list_responses':\
 [{'consumer': 'Terry', 'drink': 'beer', 'response_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}},\
 {'consumer': 'John', 'response_function': 'menu2', \
'results': [{'ingredients_res': ['egg', 'spam']}, {'ingredients_res': [\
'tomato', 'spam', 'bacon']}]},\
 {'consumer': 'Graham', 'drink': 'coffee', 'response_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},\
 {'consumer': 'Eric', 'drink': 'beer', 'response_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}},\
 {'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy', \
'response_function': 'royal_menu', \
'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}],\
 'service_time': 300}

Here the same class structure as :class:`~.parse.T4Parser` is needed, a
:obj:`collections.namedtuple` is built to fulfill this condition (only with
the needed members). This also means a Scan matching class:

>>> from collections import namedtuple
>>> ScanTup = namedtuple('ScanTup', ['countwarnings', 'counterrors', 'tasks',
...                                  'normalend', 'reqbatchs', 'times'])
>>> ntscan = ScanTup(1, 0, 1, True, 42,
...                  {'order_time': 120, 'service_time': [300]})
>>> ParseTup = namedtuple('ParseTup', ['scan_res', 'result'])
>>> ntres = ParseTup(scan_res=ntscan, result=[pres])

Construction accessor and responses book:

>>> t4acc = Accessor(ntres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
Found a responses book
>>> print(t4acc.resp_book)
ResponseBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'index', \
'response_function']

Examples of use:

>>> menu_with_dessert = t4acc.get_by(dessert=3)
>>> pprint(menu_with_dessert)  # doctest: +NORMALIZE_WHITESPACE
[{'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy', 'index': 4,\
 'response_function': 'royal_menu', \
 'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
>>> batch = t4acc.edition_batch_number()
>>> print(batch)
42
>>> simu_time = t4acc.simulation_time()
>>> print(simu_time)
-1

If no list of results, as a list of dictionaries, is avalaible (for example in
some creation runs):

>>> pres = {'edition_batch_number': 42, 'simulation_time': 4242,
...         'service_time': 300}
>>> ntscan.times['simulation_time'] = [4242]
>>> ntres = ParseTup(scan_res=ntscan, result=[pres])
>>> t4acc = Accessor(ntres)
>>> # An error is emitted as no list is available under the keys (so no
>>> # possible result)
>>> if t4acc.resp_book:
...    print("Found a responses book")
... else:
...    print("Did not found a responses book")
Did not found a responses book
>>> t4acc.edition_batch_number()
42
>>> t4acc.simulation_time()
4242

.. todo::

    Should we remove this restriction and return the globals in that case and
    an empty list of responses and empty index?


Any key allows the construction of the ResponseBook as far as the corresponding
value is a list of dictionary. The results or metadata not given in a shape of
list of dictinary are stored under the ``globals`` of the ResponseBook.

>>> pres2 = {'edition_batch_number': 42, 'and_these_are_our_meals': orders,
...          'service_time': 300}
>>> ntres2 = ParseTup(scan_res=ntscan, result=[pres2])
>>> t4acc2 = Accessor(ntres2)
>>> print(t4acc2.resp_book)
ResponseBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'index', \
'response_function']
>>> pprint(t4acc2.resp_book.globals)  # doctest: +NORMALIZE_WHITESPACE
{'edition_batch_number': 42, 'errors': 0, 'normal_end': True,\
 'number_of_tasks': 1, 'order_time': 120, 'required_batches': 42,\
 'service_time': 300, 'simulation_time': 4242, 'warnings': 1}



Module API
----------
'''

import logging
from ..response_book import ResponseBook


LOGGER = logging.getLogger('valjean')


class Accessor:
    '''Class to access T4 results in a friendly way.

    This class contains two members:

        * parsed_res = result from parsing for only one batch
        * :class:`.response_book.ResponseBook` corresponding to the list of
            responses if it exists
    '''

    def __init__(self, t4res, *, batch_id=-1, batch_number=None):
        '''Create an :class:`Accessor` from a list of responses.

        :param list(dict) t4res: result from parsing (for the moment not
                                       the result from scan, so some things
                                       might be missing like initialization
                                       time)
        '''
        if batch_number:
            batch_id = (-1 if len(t4res.result) == 1
                        else t4res.scan_res.index(batch_number))
        self.parsed_res = t4res.result[batch_id]
        glob_vars = {k: v for k, v in self.parsed_res.items()
                     if not isinstance(v, list)}
        # sanity check
        time_key = [k for k in glob_vars if 'time' in k][0]
        if glob_vars[time_key] != t4res.scan_res.times[time_key][batch_id]:
            raise ValueError('{} looks inconsistent between parsing and '
                             'scanning'.format(time_key))
        glob_vars.update(self._add_scan_vars(t4res.scan_res, batch_id,
                                             glob_vars))
        list_resps = [resp for key, lresp in self.parsed_res.items()
                      if key not in glob_vars for resp in lresp]
        self.resp_book = ResponseBook(list_resps, global_vars=glob_vars)
        if self.resp_book:
            LOGGER.debug("RESP_BOOK exists")
        else:
            LOGGER.error('ResponseBook creation failed, please check')

    @staticmethod
    def _add_scan_vars(res, batch, global_vars):
        scan_vars = {'warnings': res.countwarnings,
                     'errors': res.counterrors,
                     'number_of_tasks': res.tasks,
                     'normal_end': res.normalend,
                     'required_batches': res.reqbatchs}
        for time, val in res.times.items():
            if time not in global_vars:
                scan_vars.update({time: val} if isinstance(val, int)
                                 else {time: val[batch]})
        return scan_vars

    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (response_function, score_name, scoring_zone_id, etc).

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`~valjean.eponine.response_book.ResponseBook`
          (subset of the default one, corresponding to the selection)
        '''
        return self.resp_book.select_by(**kwargs)

    def simulation_time(self):
        '''Return simulation time.'''
        return self.parsed_res.get('simulation_time', -1)

    def edition_batch_number(self):
        '''Return edition batch number.'''
        return self.parsed_res.get('edition_batch_number', '?')
