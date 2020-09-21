r'''Module to deal with ROOT outputs from Tripoli-4 in depletion mode.

.. _the ROOT website: https://root.cern/


This module is an interface with Tripoli-4 depletion results, stored as
``ROOT`` files, see the Tripoli-4 user guide and `the ROOT website`_ for more
details.

The available results match the usual Tripoli-4 results from depletion:

* k\ :sub:`eff` as ``kcoll``, ``ktrack``, ``kstep``;
* β\_:sub:`eff` from prompt and Nauchi, called ``beff_prompt`` and
  ``beff_nauchi``;
* renormalisation factor, called ``renorm``
* total power
* power
* local burnup
* flux: fast neutron flux (``fast_flux``), thermal neutron flux
  (``therm_flux``) and total flux (``flux``)
* mass
* concentration
* activity
* reaction rates: for fast neutrons (``fast_reaction_rate``), for thermal
  neutrons (``thermal_reaction_rate``) and for one group (``reaction_rate``).
  The thermal group only gives non-zero results for fission rate.

Some of these results can be accessed from valjean using the
:class:`DepletionReader` class from this module. In some cases, it is necessary
to provide keyword for the composition name (``componame``), the isotope name
(``isotope``) or the reaction name (``reaction``).

Results can be obtained at a given depletion step (so a scalar value) or for
all available steps, giving in both cases a
:class:`~valjean.eponine.dataset.Dataset`. The access method of the array ends
with ``_time`` if the required quantity is given in function of *time* and
``_burnup`` if it is in function of *burnup*.

A typical example of use of this module is the following:

.. code-block:: python

    from valjean.eponine.tripoli4.depletion import DepletionReader
    depr = DepletionReader.from_evolution_steps(
        'evolution_1.root', 'evolution_2.root',
        root_build='/path/where/to/build/root/libraries')
    # get kstep at step 1
    kstep = depr.kstep(1)
    # get kstep as a function of burnup
    akstep = depr.kstep_burnup()
    # get total power as a function of time
    atotpow = depr.total_power_time()
    # get U238 concentration in composition COMPO1 at step 5
    conc_u238 = depr.concentration(step=5, componame='COMPO1', isotope='U238')
    # get U238 fission reaction rate in composition COMP1 as a function of time
    reac_u238 = depr.reaction_rate_time(componame='COMP1', isotope='U238',
                                        reaction='REAMT18')

Some helper methods provide the list of compositions, the list of isotopes in a
given composition or the reaction rates associated to a given isotope in a
given composition.
'''

# pylint: disable=no-member

import re
from collections import OrderedDict
from pathlib import Path
import pkg_resources as pkg
import numpy as np
from ..dataset import Dataset
from ... import LOGGER


def title_to_snake_case(word):
    '''Convert `word` from title case to snake case.

    >>> title_to_snake_case('ThisIsATitle')
    'this_is_a_title'
    '''
    word = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', word).lower()


def generic_docstrings(res_type, *list_params):
    '''Define generic docstrings for the access functions of depleted results.
    '''
    docstrings = []
    if res_type == 'value':
        docstrings.extend([
            'Return the value of {thing} from the MeanBurnupResults object.\n',
            ':param int step: the index of the calculation step'])
    else:
        if res_type == 'burnup':
            docstrings.extend([
                'Return the {thing} from the MeanBurnupResults object as a '
                'function of burnup.\n'])
        elif res_type == 'time':
            docstrings.extend([
                'Return the {thing} from the MeanBurnupResults object as a '
                'function of time.\n'])
        else:
            raise DepletionReaderException('Not foreseen result type: {}'
                                           .format(res_type))
        docstrings.append(
            '''.. note::

            The unit of the x-axis is not currently preserved as units are not
            taken into account in :class:`~valjean.eponine.dataset.Dataset`.

            ''')

    docstrings_params = {
        'componame': ':param str componame: composition name for {thing}',
        'isotope': ':param str isotope: isotope which {thing} is required',
        'reaction': ':param str reaction: reaction name'}

    docstrings.extend([docstrings_params[lpar] for lpar in list_params])

    if res_type == 'value':
        docstrings.extend([
            ':returns: {thing} and error for the given step',
            ':rtype: Dataset'])
    elif res_type == 'burnup':
        docstrings.extend([
            ":returns: {thing} and error as a function of burnup steps",
            ":rtype: Dataset"])
    else:
        docstrings.extend([
            ":returns: {thing} and error as a function of time steps",
            ":rtype: Dataset"])

    return '\n'.join(docstrings)


def add_accessors(dict_res):
    '''Automatic construction of result accessors.'''

    def decorator(cls):
        def method_factory(name, *args):
            '''Produce methods for the decorated class.

            This function takes as an argument the name of a quantity to
            retrieve from the ``MeanBurnupResults`` object. It returns three
            methods (burnup, time and value) that can be added as
            accessors to `cls`.'''
            kwargs = {arg: None for arg in args}

            def burnup_method(self, **kwargs):
                mbr_method_name = 'Get' + name + 'Histogram'
                method = getattr(self.mbr, mbr_method_name)
                # burnup -> index=0
                hist = method(**kwargs, index=0)
                return Dataset(
                    value=np.array(hist.values.data()),
                    error=np.array(hist.errors.data()),
                    bins=OrderedDict([(hist.xname,
                                       np.array(hist.bins.data()))]),
                    what=hist.yname)
            burnup_method.__doc__ = generic_docstrings(
                'burnup', *args).format(thing=name)

            def time_method(self, **kwargs):
                mbr_method_name = 'Get' + name + 'Histogram'
                method = getattr(self.mbr, mbr_method_name)
                # time -> index=1
                hist = method(**kwargs, index=1)
                return Dataset(
                    value=np.array(hist.values.data()),
                    error=np.array(hist.errors.data()),
                    bins=OrderedDict([(hist.xname,
                                       np.array(hist.bins.data()))]),
                    what=hist.yname)
            time_method.__doc__ = generic_docstrings(
                'time', *args).format(thing=name)

            def value_method(self, step, **kwargs):
                mbr_method_name = 'Get' + name
                method = getattr(self.mbr, mbr_method_name)
                value = method(step, *list(kwargs.values()), 0)
                error = method(step, *list(kwargs.values()), 1)
                return Dataset(value=np.float_(value), error=np.float_(error))
            value_method.__doc__ = generic_docstrings(
                'value', *list(kwargs.keys())).format(thing=name)

            return burnup_method, time_method, value_method

        for name, args in dict_res.items():
            sc_name = title_to_snake_case(name)
            bu_method, time_method, value_method = method_factory(name, *args)
            setattr(cls, sc_name + '_burnup', bu_method)
            setattr(cls, sc_name + '_time', time_method)
            setattr(cls, sc_name, value_method)
        return cls
    return decorator


@add_accessors({
    'Kcoll': [],
    'Ktrack': [],
    'Kstep': [],
    'BeffPrompt': [],
    'BeffNauchi': [],
    'Renorm': [],
    'TotalPower': [],
    'Power': ['componame'],
    'LocalBurnup': ['componame'],
    'FastFlux': ['componame'],
    'ThermFlux': ['componame'],
    'Mass': ['componame', 'isotope'],
    'Concentration': ['componame', 'isotope'],
    'Activity': ['componame', 'isotope'],
    'ReactionRate': ['componame', 'isotope', 'reaction'],
    'FastReactionRate': ['componame', 'isotope', 'reaction'],
    'ThermalReactionRate': ['componame', 'isotope', 'reaction']})
class DepletionReader:
    '''Class to use depletion results from Tripoli-4'''

    def __init__(self, mbr):
        '''Initialisation of DepletionReader.

        :param mbr: MeanBurnupResult
        '''
        self.mbr = mbr

    @staticmethod
    def init_postscripts(root_build=""):
        '''Initialize postscripts from ROOT macros.

        ROOT macros are in the `resources/depletion` folder. They are compiled
        in the `__t4depletion__` folder to used afterwards.
        '''
        try:
            import ROOT
        except ImportError as ierr:
            LOGGER.error('ROOT needs to be added to PYTHONPATH')
            raise ImportError('ROOT missing') from ierr
        ps_fold = 'valjean.eponine.tripoli4.resources.depletion'
        assert pkg.resource_exists(ps_fold, 'DepletedComposition.C')
        assert pkg.resource_exists(ps_fold, 'BurnupResults.C')
        assert pkg.resource_exists(ps_fold, 'MeanBurnupResults.C')
        fname = pkg.resource_filename(ps_fold, 'DepletedComposition.C')
        path_fname = Path(fname)
        ROOT.gROOT.SetMacroPath(str(path_fname.parent))
        if not root_build:
            LOGGER.warning('T4 depletion postscripts ROOT libraries will be '
                           'compiled in valjean folder, permissions might not '
                           'be granted.')
            root_build = path_fname.parent / "__t4depletion__"
        ROOT.gSystem.MakeDirectory(str(root_build))
        ROOT.gSystem.SetBuildDir(str(root_build), True)
        ROOT.gROOT.LoadMacro('DepletedComposition.C+')
        ROOT.gROOT.LoadMacro('BurnupResults.C+')
        ROOT.gROOT.LoadMacro('MeanBurnupResults.C+')
        return ROOT

    @classmethod
    def from_evolution_steps(cls, *fnames, root_build=""):
        '''Initialisation from `evolution.root` files (one per simulation).

        :param str fnames: ROOT files
        '''
        root = cls.init_postscripts(root_build)
        cls.fnames = fnames
        lmbr = root.MeanBurnupResults()
        for fname in fnames:
            lmbr.AddSimulationAndProcess(fname)
        return cls(mbr=lmbr)

    @classmethod
    def from_mbr(cls, fname, mbr_name, root_build=""):
        '''Initialisation from ROOT file containing a MeanBurnupResults class.

        :param str fname: ROOT file name
        :param str mbr_name: name of the MeanBurnupResults object in the file
        '''
        root = cls.init_postscripts(root_build)
        cls.fname = fname
        tfname = root.TFile(fname)
        lmbr = tfname.Get(mbr_name)
        tfname.Close()
        return cls(mbr=lmbr)

    def save_mbr(self, name):
        '''Save the MeanBurnupResults in a ROOT file.

        :param str name: name of the output ROOT file name
        '''
        self.mbr.SaveAs(name)

    def nb_simu(self):
        '''Return the number of independent simulations.

        :rtype: int
        '''
        return self.mbr.GetNbSimu()

    def nb_compositions(self):
        '''Return the number of compositions.

        :rtype; int
        '''
        return self.mbr.GetNbCompos()

    def nb_steps(self):
        '''Return the number of steps.

        :rtype: int
        '''
        return self.mbr.GetSteps()

    def burnup(self, step):
        r'''Return burnup from MeanBurnupResults object.

        :param int step: calculation step to use to get the value
        :returns: burnup value and error
        :rtype: Dataset
        '''
        return Dataset(value=np.float_(self.mbr.GetBurnup(step, 0)),
                       error=np.float_(self.mbr.GetBurnup(step, 1)))

    def burnup_array(self):
        r'''Return burnup array from MeanBurnupResults object.

        :returns: burnup value and error by step
        :rtype: Dataset
        '''
        val, err = [], []
        steps = list(range(1, self.mbr.GetSteps()+1))
        for i in steps:
            val.append(self.mbr.GetBurnup(i, 0))
            err.append(self.mbr.GetBurnup(i, 1))
        return Dataset(
            value=np.array(val), error=np.array(err),
            bins=OrderedDict([('step', np.array(steps))]))

    def time(self, step):
        r'''Return time from MeanBurnupResults object.

        :param int step: calculation step to use to get the value
        :returns: time value and error
        :rtype: Dataset
        '''
        return Dataset(value=np.float_(self.mbr.GetTime(step, 0)),
                       error=np.float_(self.mbr.GetTime(step, 1)))

    def time_array(self):
        r'''Return time array from MeanBurnupResults object.

        :returns: time value and error by step
        :rtype: Dataset
        '''
        val, err = [], []
        steps = list(range(1, self.mbr.GetSteps()+1))
        for i in steps:
            val.append(self.mbr.GetTime(i, 0))
            err.append(self.mbr.GetTime(i, 1))
        return Dataset(
            value=np.array(val), error=np.array(err),
            bins=OrderedDict([('step', np.array(steps))]))

    def composition_names(self):
        '''Return the list of composition names.

        :rtype: list(str)
        '''
        lcomp = [self.mbr.GetDepletedCompositionName(i)
                 for i in range(1, self.nb_compositions()+1)]
        return lcomp

    def isotope_names(self, step, componame):
        '''Return the list of isotopes in the given composition at the given
        step.

        :param int step: calculation step to use to get the value
        :param str componame: composition name in which list of isotopes is
            required
        :returns: list of available isotopes
        :rtype: list(str)
        '''
        depli = list(self.mbr.GetDepletedIsotopeNames(step, componame))
        return [str(iso) for iso in depli]

    def reaction_names(self, step, componame, isotope):
        '''Get reaction names in composition for the given isotope.

        :param int step: calculation step to use to get the value
        :param str componame: composition name where reaction is required
        :param str isotope: isotope name for which reaction is required
        :returns: list of available reactions
        :rtype: list(str)
        '''
        srn = self.mbr.GetDepletedReactionNames(step, componame, isotope)
        return [str(i) for i in srn]

    def isotope_reaction_names(self, step, componame):
        '''Get dictionary of reactions per isotope for the given step and
        composition.

        :param int step: calculation step to use to get the value
        :param str componame: composition name where reactions per isotope are
            required
        :returns: reactions by isotopes
        :rtype: dict(str, list(str))
        '''
        lir = self.mbr.GetDepletedIsotopeReactionNames(step, componame)
        return {i: [str(r) for r in setr] for i, setr in lir}

    def dump_global_results(self, step):
        '''Print results for a given step.

        This includes compositions.
        '''
        self.mbr.DumpGlobalResults(step)


class DepletionReaderException(Exception):
    '''An error that may be raised by the :class:`DepletionReader` class.'''
