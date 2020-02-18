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
from .verbosity import Verbosity


class Representation:
    '''Class for representing test results as templates calling the available
    representers (tables or plots).

    This class corresponds to the `Context` role in the `Strategy` design
    pattern.
    '''

    def __init__(self, representer, verbosity=None):
        ''''Initilialisation of the :class:`Representation` class with the
        Representer to use.

        :param Representer: representer to use (table, plots, both, etc)
        :type representer: :class:`Representer`
        '''
        self.representer = representer
        self.verbosity = verbosity

    def __call__(self, result):
        '''Dispatch handling of `result` to the ``__call__`` methods of the
        representer class.'''
        if callable(self.verbosity):
            verbosity = self.verbosity(result)
        else:
            verbosity = self.verbosity
        res = self.representer(result, verbosity)
        if res is None:
            return []
        LOGGER.debug('representing the result of test %s as %s',
                     result.test.name, res)
        return res


class Representer:
    '''Base class for representing test results as templates (in the sense of
    the :mod:`~.templates` module).

    This class corresponds to the `Strategy` role in the `Strategy` design
    pattern. Its subclasses play the role of `ConcreteStrategy`.
    '''

    def __call__(self, result, verbosity=None):
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
            LOGGER.debug('no representer for class %s with name %s',
                         class_name, meth_name)
            return None
        return meth(result, verbosity)


class TableRepresenter(Representer):
    '''This class is the default representation class for tables. It contains
    the overridden :meth:`Representer.__call__`.

    Advice: users willing to customize the behaviour of TableRepresenter for
    specific test results should subclass TableRepresenter and define the
    relevant ``repr_*`` methods.
    '''

    def __call__(self, result, verbosity=None):
        LOGGER.debug("In TableRepresenter.__call__, %s", verbosity)
        res = super().__call__(result, verbosity)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            try:
                meth = getattr(tab_elts, meth_name)
            except AttributeError:
                LOGGER.info('no table representer %s', meth_name)
                return None
            res = meth(result, verbosity)
        return res


class FullTableRepresenter(TableRepresenter):
    '''Class to define the specific methods for full representation of tables.
    This only involve few cases needing the :meth:`TableRepresenter.__call__`
    method like in Bonferroni and Holm-Bonferroni test results.
    '''

    def repr_testresultbonferroni(self, result, verbosity=None):
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
        if verbosity == Verbosity.SILENT:
            return tab_elts.repr_testresultholmbonferroni(result, verbosity)
        ftest_verb = (Verbosity(verbosity.value-1)
                      if verbosity not in (Verbosity.SILENT, None)
                      else verbosity)
        return (super().__call__(result.first_test_res, ftest_verb)
                + tab_elts.repr_testresultbonferroni(result, verbosity))

    def repr_testresultholmbonferroni(self, result, verbosity=None):
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
        if verbosity == Verbosity.SILENT:
            return tab_elts.repr_testresultholmbonferroni(result, verbosity)
        ftest_verb = (Verbosity(verbosity.value-1)
                      if verbosity not in (Verbosity.SILENT, None)
                      else verbosity)
        return (super().__call__(result.first_test_res, ftest_verb)
                + tab_elts.repr_testresultholmbonferroni(result, verbosity))


class PlotRepresenter(Representer):
    '''This class is the default representation class for plots. It contains
    the overridden :meth:`Representer.__call__`.

    Advice: users willing to customize the behaviour of
    :class:`PlotRepresenter` for specific test results should subclass
    :class:`PlotRepresenter` and define the relevant ``repr_*`` methods.
    '''
    def __init__(self, post=plt_elts.post_treatment):
        self.post = post
        if self.post is not None or not callable(self.post):
            LOGGER.warning('Plot post-treatment shoould be a callable.')

    def __call__(self, result, verbosity=None):
        LOGGER.debug("In PlotRepresenter.__call__")
        res = super().__call__(result, verbosity)
        if res is None:
            class_name = result.__class__.__name__
            meth_name = 'repr_' + class_name.lower()
            try:
                meth = getattr(plt_elts, meth_name)
            except AttributeError:
                LOGGER.info('no plot representer %s', meth_name)
                return None
            res = meth(result, verbosity)
        if res and self.post is not None:
            res = self.post(res, result)
        return res

    def repr_testresultbonferroni(self, result, verbosity=None):
        '''Represent the result of a :class:`~.TestBonferroni` test one a plot
        (only the input test for the moment) (Student, equal, etc)

        :param  result: a test result.
        :type result: :class:`~.TestResultBonferroni`
        :returns: Representation of a :class:`~.TestResultBonferroni` as
            1 plot (the first test result).
        :rtype: list(:class:`~.PlotTemplate`)
        '''
        LOGGER.debug("In FullPlotRepresenter.repr_testresultbonferroni")
        return self(result.first_test_res, verbosity)

    def repr_testresultholmbonferroni(self, result, verbosity=None):
        '''Represent the result of a :class:`~.TestHolmBonferroni` test as a
        plot (Student, equal, etc)

        :param  result: a test result.
        :type result: :class:`~.TestResultHolmBonferroni`
        :returns: Representation of a :class:`~.TestResultHolmBonferroni` as
            a plot (the first test result).
        :rtype: list(:class:`~.PlotTemplate`)
        '''
        LOGGER.debug("In PlotRepresenter.repr_testresultholmbonferroni")
        return self(result.first_test_res, verbosity)


class FullPlotRepresenter(PlotRepresenter):
    '''Class to define the specific methods for full representation of plots.
    This only involve few cases needing the :meth:`PlotRepresenter.__call__`
    method like in Bonferroni and Holm-Bonferroni test results.
    '''

    def repr_testresultbonferroni(self, result, verbosity=None):
        '''Represent the result of a :class:`~.TestBonferroni` test one a plot
        (only the input test for the moment) (Student, equal, etc)

        :param  result: a test result.
        :type result: :class:`~.TestResultBonferroni`
        :returns: Representation of a :class:`~.TestResultBonferroni` as
            1 plot (the first test result).
        :rtype: list(:class:`~.PlotTemplate`)
        '''
        LOGGER.debug("In FullPlotRepresenter.repr_testresultbonferroni")
        return self(result.first_test_res, verbosity)

    def repr_testresultholmbonferroni(self, result, verbosity=None):
        '''Represent the result of a :class:`~.TestHolmBonferroni` test as a
        plot (Student, equal, etc)

        :param  result: a test result.
        :type result: :class:`~.TestResultHolmBonferroni`
        :returns: Representation of a :class:`~.TestResultHolmBonferroni` as
            a plot (the first test result).
        :rtype: list(:class:`~.PlotTemplate`)
        '''
        LOGGER.debug(
            "In FullPlotRepresenter.repr_testresultholmbonferroni")
        return self(result.first_test_res, verbosity)


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
        self.plot_repr = FullPlotRepresenter()

    def __call__(self, result, verbosity=None):
        '''Dispatch handling of `result` to all the Representer subclass
        instance attributes of :class:`FullRepresenter`, based on the name of
        the class of `result`.

        If the representer does not exist in :mod:`~.table_elements` or
        :mod:`~.plot_elements` a ``None`` is returned and replaced here by an
        empty list. If none of them exist the global return will be an empty
        list (no ``None`` returned from this step).
        '''
        res = []
        tabres = self.table_repr(result, verbosity)
        if tabres is not None:
            res.extend(tabres)
        pltres = self.plot_repr(result, verbosity)
        if pltres is not None:
            res.extend(pltres)
        return res
