'''
Module to access Tripoli-4 parsed results.

  * :class:`Accessor` that allows to access and select in easier way the
    various elements of the parsing results, using internally the 2 follwing
    classes;


:class:`Accessor`
-----------------

The :class:`Accessor` class is the real access point to the list of responses
but not only. The result from parsing is its default input. This parsing result
is necessarly a dictionary, i.e. if you get a list of dictionary because you
required to parse more than one batch you'll need to access them thanks to a
loop over the list of batches. Accessor also allows simplified access to other
data like simulation time or number of batch.

For example, let's consider a parsing results that contains the same ``orders``
as in :mod:`.responses_book`, represented as a list of dictionaries. It will be
stored under the key ``'list_responses'`` and additional items will be added to
that dictionary for it to look like a default parsing results one.

>>> from valjean.eponine.tripoli4.accessor import Accessor
>>> from pprint import pprint
>>> orders = [
... {'resp_function': 'menu1', 'consumer': 'Terry', 'drink': 'beer',
...  'results': {'ingredients_res': ['egg', 'bacon']}},
... {'resp_function': 'menu2', 'consumer': 'John',
...  'results': [{'ingredients_res': ['egg', 'spam']},
...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
... {'resp_function': 'menu1', 'consumer': 'Graham', 'drink': 'coffee',
...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
... {'resp_function': 'menu3', 'consumer': 'Eric', 'drink': 'beer',
...  'results': {'ingredients_res': ['sausage'],
...              'side_res': 'baked beans'}},
... {'resp_function': 'royal_menu', 'consumer': 'Michael',
...  'drink': 'brandy', 'dessert': 3,
...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
>>> pres = {'edition_batch_number': 42, 'list_responses': orders}
>>> pprint(pres)  # doctest: +NORMALIZE_WHITESPACE
{'edition_batch_number': 42, 'list_responses':\
 [{'consumer': 'Terry', 'drink': 'beer', 'resp_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}},\
 {'consumer': 'John', 'resp_function': 'menu2', \
'results': [{'ingredients_res': ['egg', 'spam']}, {'ingredients_res': [\
'tomato', 'spam', 'bacon']}]},\
 {'consumer': 'Graham', 'drink': 'coffee', 'resp_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},\
 {'consumer': 'Eric', 'drink': 'beer', 'resp_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}},\
 {'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy', \
'resp_function': 'royal_menu', 'results': {'dish_res': ['lobster thermidor', \
'Mornay sauce']}}]}

Construction accessor and responses book:

>>> t4acc = Accessor(pres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
Found a responses book
>>> print(t4acc.resp_book)
ResponsesBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'resp_function']

Examples of use:

>>> menu_with_dessert = t4acc.get_by(dessert=3)
>>> pprint(menu_with_dessert)  # doctest: +NORMALIZE_WHITESPACE
[{'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy',\
 'resp_function': 'royal_menu', 'results': {'dish_res': ['lobster thermidor',\
 'Mornay sauce']}}]
>>> batch = t4acc.edition_batch_number()
>>> print(batch)
42
>>> simu_time = t4acc.simulation_time()
>>> print(simu_time)
-1

If no list of responses is avalaible (for example in some creation runs):

>>> pres = {'edition_batch_number': 42, 'simulation_time': 4242}
>>> t4acc = Accessor(pres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
... else:
...    print("Did not found a responses book")
Did not found a responses book
>>> t4acc.edition_batch_number()
42
>>> t4acc.simulation_time()
4242
'''

import logging
from ..responses_book import ResponsesBook


LOGGER = logging.getLogger('valjean')


class Accessor:
    '''Class to access T4 results in a friendly way.

    This class contains two members:

        * parsed_res = result from parsing for only one batch
        * :class:`.responses_book.ResponsesBook` corresponding to the list of
            responses if it exists
    '''

    def __init__(self, tparsed_res):  # , merge_score=False):
        '''Create an :class:`Accessor` from a list of responses.

        :param list(dict) tparsed_res: result from parsing (for the moment not
                                       the result from scan, so some things
                                       might be missing like initialization
                                       time)
        '''
        self.parsed_res = tparsed_res
        self.resp_book = (ResponsesBook(self.parsed_res['list_responses'])
                          if 'list_responses' in self.parsed_res
                          else None)
        if self.resp_book:
            LOGGER.debug("RESP_BOOK exists")

    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (resp_function, score_name, scoring_zone_id, etc).

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`~valjean.eponine.responses_book.ResponsesBook`
          (subset of the default one, corresponding to the selection)
        '''
        return self.resp_book.select_by(**kwargs)

    def simulation_time(self):
        '''Return simulation time.'''
        return self.parsed_res.get('simulation_time', -1)

    def edition_batch_number(self):
        '''Return edition batch number.'''
        return self.parsed_res.get('edition_batch_number', '?')
