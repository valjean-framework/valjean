'''This module contains code that converts a test result into some kind of
human-readable representation (table, plots, etc.).

.. todo::

    Possible improvement: turn :class:`Representer` into an `ABC`; loop over
    the classes in :mod:`~.eponine` that inherit from `:class:`~.TestResult`
    and add `@abstractmethod` methods in :class:`Representer`. This way, if
    a new :class:`~.TestResult` is added to :mod:`~.eponine`, it will no longer
    be possible to instantiate any of the classes that derive from
    :class:`Representer`, pointing to the fact that the code in this module
    needs to be extended to handle the new class. This is better than silently
    falling back to some default do-nothing implementation, which may lead to
    bugs.


This module uses the `Strategy` design pattern. The :class:`Representation`
class plays the role of `Context`,  :class:`Representer` plays the role of
`Strategy` and the classes derived from :class:`Representer` (such as
:class:`TableRepresenter`, :class:`PlotRepresenter`, etc.) play the role of
`ConcreteStrategy`. See E. Gamma et al., "Design Patterns" (1995),
ISBN 0-201-63361-2, Addison-Weasley, USA.


Currently we have 3 main ``Representer`` classes:

* :class:`Representer`: parent class of all others, containing the default
  :meth:`Representer.__call__` method, calling the class method named
  ``'repr_' + class.name`` of the test;
* :class:`TableRepresenter`: inherited from :class:`Representer`,
  designed as a parent class for user's own representations of tables. Its
  :meth:`TableRepresenter.__call__` method first looks for a method called
  ``'repr_' + class.name``; if it does not exist call the default method from
  the catalogue of table representation accessible in :mod:`.table_elements`;
* :class:`PlotRepresenter`: inherited from :class:`Representer`, designed
  as a parent class for user's own representations of plots. Its
  :meth:`PlotRepresenter.__call__` method first looks for a method called
  ``'repr_' + class.name``; if it does not exist call the default method from
  the catalogue of plot representation accessible in :mod:`.plot_elements`.


An example of use of the ``Representer`` objects can be seen in the
:class:`FullTableRepresenter`. In this table representation, for the Bonferroni
test result, the input test result is first represented in a table, then the
Bonferroni itself is represented in a second table.


Thus the use of the ``Representer`` is foreseen as:

* use the default methods provided in :class:`TableRepresenter` and
  :class:`PlotRepresenter`;
* if customisation is needed, you can easily call the additional method
  available in :mod:`.table_elements` and :mod:`.plot_elements`;
* you can also write your own representation method provided they follow the
  naming convention ``'repr_' + class.name``;
* :mod:`valjean` calls the ``Representer`` classes through the
  :class:`Representation` class.
'''
from .. import LOGGER
from . import table_elements as tab_elts
from . import plot_elements as plt_elts


class Representation:
    '''Class for representing test results as templates calling the available
    patterns (tables or plots).

    This class corresponds to the `Context` role in the `Strategy` design
    pattern.
    '''

    def __init__(self, pattern):
        ''''Initilialisation of the :class:`Representation` class with the
        pattern to use.

        :param pattern: pattern to be used (table, plots, both, etc)
        :type pattern: :class:`Representer` or subclass from
            :class:`Representer`.
        '''
        self.pattern = pattern

    def __call__(self, result):
        '''Dispatch handling of `result` to the ``__call__`` methods of the
        pattern class.'''
        res = self.pattern(result)
        if res is None:
            return []
        return res


class Representer:
    '''Base class for representing test results as templates (in the sense of
    the :mod:`~.templates` module).

    This class corresponds to the `Strategy` role in the `Strategy` design
    pattern. Its subclasses play the role of `ConcreteStrategy`.
    '''

    def __call__(self, result):
        '''Dispatch handling of `result` to the appropriate subclass method,
        based on the name of the class of `result`. This methods essentially
        implements a simplified, run-time version of the Visitor pattern.
        '''
        LOGGER.debug("In Representer.__call__")
        class_name = result.__class__.__name__
        meth_name = 'repr_' + class_name.lower()
        try:
            meth = getattr(self, meth_name)
        except AttributeError:
            LOGGER.debug('no representation for class %s', class_name)
            return None
        return meth(result)


class TableRepresenter(Representer):
    '''This class is the default representation class for tables. It contains
    the overridden :meth:`Representer.__call__`.

    Advice: users willing to customize the behaviour of TableRepresenter for
    specific test results should subclass TableRepresenter and define the
    relevant ``repr_*`` methods.
    '''

    def __call__(self, result):
        LOGGER.debug("In TableRepresenter.__call__")
        res = super().__call__(result)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            try:
                meth = getattr(tab_elts, meth_name)
            except AttributeError:
                LOGGER.info('no table representation for class %s', class_name)
                return None
            res = meth(result)
        return res


class FullTableRepresenter(TableRepresenter):
    '''Class to define the specific methods for full representation of tables.
    This only involve few cases needing the :meth:`TableRepresenter.__call__`
    method like in Bonferroni and Holm-Bonferroni test results.
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
        :rtype: list(:class:`~.TableTemplate`)
        '''
        LOGGER.debug("In FullTableRepresenter.repr_testresultbonferroni")
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
        :rtype: list(:class:`~.TableTemplate`)
        '''
        LOGGER.debug(
            "In FullTableRepresenter.repr_testresultholmbonferroni")
        return (super().__call__(result.first_test_res)
                + tab_elts.repr_testresultholmbonferroni(result))


class PlotRepresenter(Representer):
    '''This class is the default representation class for plots. It contains
    the overridden :meth:`Representer.__call__`.

    Advice: users willing to customize the behaviour of
    :class:`PlotRepresenter` for specific test results should subclass
    :class:`PlotRepresenter` and define the relevant ``repr_*`` methods.
    '''

    def __call__(self, result):
        LOGGER.debug("In PlotRepresenter.__call__")
        res = super().__call__(result)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            try:
                meth = getattr(plt_elts, meth_name)
            except AttributeError:
                LOGGER.info('no plot representation for class %s', class_name)
                return None
            res = meth(result)
        return res


class FullPlotRepresenter(PlotRepresenter):
    '''Class to define the specific methods for full representation of plots.
    This only involve few cases needing the :meth:`PlotRepresenter.__call__`
    method like in Bonferroni and Holm-Bonferroni test results.
    '''


class EmptyRepresenter(Representer):
    '''Class that does not generate any templates for any test result.'''


class FullRepresenter(Representer):
    '''This class generates the fullest possible representation for test
    results. If anything can be represented as an template,
    :class:`FullRepresenter` will do it.
    '''

    def __init__(self):
        '''Initialisation of :class:`FullRepresenter`.

        Two instance objects are built: a :class:`FullTableRepresenter` and
        a :class:`PlotRepresenter`.
        '''
        LOGGER.debug("In initialisation of FullRepresenter")
        self.table_repr = FullTableRepresenter()
        self.plot_repr = PlotRepresenter()

    def __call__(self, result):
        '''Dispatch handling of `result` to all the Representer subclass
        instance attributes of :class:`FullRepresenter`, based on the name of
        the class of `result`.

        If the representer does not exist in :mod:`~.table_elements` or
        :mod:`~.plot_elements` a ``None`` is returned and replaced here by an
        empty list. If none of them exist the global return will be an empty
        list (no ``None`` returned from this step).
        '''
        res = []
        tabres = self.table_repr(result)
        if tabres is not None:
            res.extend(tabres)
        pltres = self.plot_repr(result)
        if pltres is not None:
            res.extend(pltres)
        return res
