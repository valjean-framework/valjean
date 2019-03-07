'''This module contains code that converts a test result into some kind of
human-readable representation (table, plots, etc.).

.. todo::

    Possible improvement: turn :class:`Representation` into an `ABC`; loop over
    the classes in :mod:`~.eponine` that inherit from `:class:`~.TestResult`
    and add `@abstractmethod` methods in :class:`Representation`. This way, if
    a new :class:`~.TestResult` is added to :mod:`~.eponine`, it will no longer
    be possible to instantiate any of the classes that derive from
    :class:`Representation`, pointing to the fact that the code in this module
    needs to be extended to handle the new class. This is better than silently
    falling back to some default do-nothing implementation, which may lead to
    bugs.


Currently we have 3 main ``Representation`` classes:

* :class:`Representation`: parent class of all others, containing the default
  :meth:`Representation.__call__` method, calling the class method named
  ``'repr_' + class.name`` of the test;
* :class:`TableRepresentation`: inherited from :class:`Representation`,
  designed as a parent class for user's own representations of tables. It's
  :meth:`TableRepresentation.__call__` method first calls the class
  representation method through the :meth:`Representation.__call__` one
  (meaning it should also be named ``'repr_' + class.name``), if it does not
  exist call the default method from the catalogue of table representation
  accessible in :mod:`.table_elements`;
* :class:`PlotRepresentation`: inherited from :class:`Representation`, designed
  as a parent class for user's own representations of plots. It's
  :meth:`PlotRepresentation.__call__` method first calls the class
  representation method through the :meth:`Representation.__call__` one
  (meaning it should also be named ``'repr_' + class.name``), if it does not
  exist call the default method from the catalogue of plot representation
  accessible in :mod:`.plot_elements`.


An example of use of the ``Representation`` objects can be seen in the
:class:`FullTableRepresentation`. For example, in this table representation for
the Bonferroni test result, the input test result is first represented in a
table, then the Bonferroni itself is represented in a second table (they cannot
be combined as different headers, see :func:`.items.concatenate`).


Thus the use of the ``Representation`` is forseen as:

* use the default methods provided in :class:`TableRepresentation` and
  :class:`PlotRepresentation`;
* if customisation is needed, you can easily call the additional method
  available in :mod:`.table_elements` and :mod:`.plot_elements`;
* you can also write your own representation method provided they follow the
  naming convention ``'repr_' + class.name``.
'''
from .. import LOGGER
from . import table_elements as tab_elts
from . import plot_elements as plt_elts


class Representation:
    '''Base class for representing test results as items (in the sense of the
    :mod:`~.items` module).'''

    def __call__(self, result):
        '''Dispatch handling of `result` to the appropriate subclass method,
        based on the name of the class of `result`. This methods essentially
        implements a simplified, run-time version of the Visitor pattern.'''
        LOGGER.debug("In Representation.__call__")
        class_name = result.__class__.__name__
        meth_name = 'repr_' + class_name.lower()
        try:
            meth = getattr(self, meth_name)
        except AttributeError:
            LOGGER.debug('no representation for class %s', class_name)
            return None
        return meth(result)


class TableRepresentation(Representation):
    '''This class is the default representation class for tables. It contains
    the overridden :meth:`Representation.__call__`.

    Advice: users TableRepresentation classes should inherit from it and not
    override the :meth:`Representation.__call__` method.
    '''

    def __call__(self, result):
        LOGGER.debug("In TableRepresentation.__call__")
        res = super().__call__(result)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            meth = getattr(tab_elts, meth_name)
            res = meth(result)
        return res


class FullTableRepresentation(TableRepresentation):
    '''Class to define the specific methods for full representation of tables.
    This only involve few cases needing the
    :meth:`TableRepresentation.__call__` method like in Bonferroni and
    Holm-Bonferroni test results.
    '''

    def repr_testresultbonferroni(self, result):
        '''Represent the result of a :class:`~.TestBonferroni` test in two
        tables:

        1. First test result (Student, equal, etc)
        2. Bonferroni test result

        :param  result: a test result.
        :type result: :class:`~.TestResultBonferroni`
        :returns: Representation of a :class:`~.TestResultBonferroni` as
            2 tables (the first test result and the Bonferroni result).
        :rtype: list(:class:`~.TableItem`)
        '''
        LOGGER.debug("In FullTableRepresentation.repr_testresultbonferroni")
        return (super().__call__(result.first_test_res)
                + tab_elts.repr_testresultbonferroni(result))

    def repr_testresultholmbonferroni(self, result):
        '''Represent the result of a :class:`~.TestHolmBonferroni` test in two
        tables:

        1. First test result (Student, equal, etc)
        2. Holm-Bonferroni test result

        :param  result: a test result.
        :type result: :class:`~.TestResultHolmBonferroni`
        :returns: Representation of a :class:`~.TestResultHolmBonferroni` as
            2 tables (the first test result and the Holm-Bonferroni result).
        :rtype: list(:class:`~.TableItem`)
        '''
        LOGGER.debug(
            "In FullTableRepresentation.repr_testresultholmbonferroni")
        return (super().__call__(result.first_test_res)
                + tab_elts.repr_testresultholmbonferroni(result))


class PlotRepresentation(Representation):
    '''This class is the default representation class for plots. It contains
    the overridden :meth:`Representation.__call__`.

    Advice: users PlotRepresentation classes should inherit from it and not
    override the :meth:`Representation.__call__` method.
    '''

    def __call__(self, result):
        LOGGER.debug("In PlotRepresentation.__call__")
        res = super().__call__(result)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            meth = getattr(plt_elts, meth_name)
            res = meth(result)
        return res


class FullPlotRepresentation(PlotRepresentation):
    '''Class to define the specific methods for full representation of plots.
    This only involve few cases needing the
    :meth:`PlotRepresentation.__call__` method like in Bonferroni and
    Holm-Bonferroni test results.
    '''


class EmptyRepresentation(Representation):
    '''Class that does not generate any items for any test result.'''

    def __call__(self, result):
        '''Dispatch handling of `result` to all the Representation subclass
        instance attributes of :class:`EmptyRepresentation`.
        Always returns an empty list.
        '''
        return []


class FullRepresentation(Representation):
    '''This class generates the fullest possible representation for test
    results. If anything can be represented as an item,
    :class:`FullRepresentation` will do it.
    '''

    def __init__(self):
        '''Initialisation of :class:`FullRepresentation`.

        Two instance objects are built: a :class:`FullTableRepresentation` and
        a :class:`PlotRepresentation`.
        '''
        LOGGER.debug("In initialisation of FullRepresentation")
        self.table_repr = FullTableRepresentation()
        self.plot_repr = PlotRepresentation()

    def __call__(self, result):
        '''Dispatch handling of `result` to all the Representation subclass
        instance attributes of :class:`FullRepresentation`, based on the name
        of the class of `result`.'''
        class_name = result.__class__.__name__
        try:
            table_res = self.table_repr(result)
        except AttributeError:
            LOGGER.debug('no table representation for class %s', class_name)
            table_res = []
        try:
            plot_res = self.plot_repr(result)
        except AttributeError:
            LOGGER.debug('no plot representation for class %s', class_name)
            plot_res = []
        return table_res + plot_res
