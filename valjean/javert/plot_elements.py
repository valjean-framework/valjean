'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
import numpy as np
from .. import LOGGER
from .templates import PlotTemplate, CurveElements, SubPlotElements, join
from .verbosity import Verbosity


# turn off pylint warnings about invalid names in this file; there are just too
# many long function names and they cannot be renamed because
# javert.representation looks for them by programmatically constructing their
# name based on the name of the test result class, the verbosity, etc.
# pylint: disable=invalid-name


def dimensions_from_array(array_shape):
    '''Check if array is consistent with 1D plot.

    Checks are done on presence of non-trivial and trivial dimensions, trivial
    being a dimension with size equal to one, non-trivial being for a dimension
    with at least two values.

    :param tuple(int) array_shape: shape of the **values** array
    :returns: indices of the non-trivial dimensions in the shape tuple
    :rtype: tuple(int)
    '''
    non_trivial_dims = tuple(d for d, s in enumerate(array_shape) if s > 1)
    LOGGER.debug("Non-trivial dimensions: %s", non_trivial_dims)
    if not non_trivial_dims:
        LOGGER.debug("Only trivial dimensions, you may prefer a different "
                     "kind of plot (PlotPoint).")
        return None
    return non_trivial_dims


def dimensions_and_bins(bins, array_shape):
    '''Determine the dimensions of the result from the
    :obj:`collections.OrderedDict` of bins. It is expected to be the "only
    non-trivial" dimensions.

    :param bins: bins coming from the results dataset
    :type bins: collections.OrderedDict(str, numpy.ndarray)
    :param tuple(int) array_shape: shape of the **values** array from the
        results dataset
    :returns: dimensions and bins to be used (non-trivial ones)
    :rtype: collections.OrderedDict
    '''
    idims = dimensions_from_array(array_shape)
    if idims is None:
        return None
    # subd = {k: v for i, (k, v) in enumerate(bins.items()) if i in idims}
    items = list(bins.items())
    subd = dict(items[i] for i in idims)
    return subd


def trim_range(bins):
    '''Adapt bins range when extreme bins are very large.

    This function suggests reasonable ranges for the given bin axes by trimming
    the extreme bins if they are too wide. For each axis, the extreme bins are
    trimmed if their width is at least 1000 times larger than the width of the
    neighbouring bin (the first bin is compared to the second one, and the last
    bin is compared to the second-last one). If there is no need to change
    the previous limits a tuple with initial limits is returned for the
    considered dimension. A boolean is associated to the tuple to precise if
    the limits have be changed.

    The trimmed ranges extend a bit over the clipped bins, so that their
    content is still visible in the plots.

    :param list(numpy.ndarray) bins: bins of the :class:`~.PlotTemplate`
    :returns: new limits for all dimensions
    :rtype: list(list(tuple(int, int), bool), list(tuple(int, int), bool), )
    '''
    LOGGER.debug('In plot_elements.trim_range')
    blimits = []
    for lbins in bins:
        nbins = lbins
        has_changed = [False, False]
        limits = [nbins[0], nbins[-1]]
        if nbins.size < 3:
            LOGGER.warning('Not enough bins to adapt range.')
            blimits.append([])
            continue
        if nbins.size < 4:
            LOGGER.warning('Will adapt range for %d bins, '
                           'binning might be not suitable')
        binw = np.ediff1d(lbins)
        if binw[0]/binw[1] > 1e3:
            limits[0] = nbins[1]
            has_changed[0] = True
        if binw[-1]/binw[-2] > 1e3:
            limits[1] = nbins[-2]
            has_changed[1] = True
        rwidth = limits[1] - limits[0]
        if has_changed[0] or len(bins) == 1:
            limits[0] -= 0.05 * rwidth
        if has_changed[1] or len(bins) == 1:
            limits[1] += 0.05 * rwidth
        blimits.append([tuple(limits), any(has_changed)])
    return blimits


def post_treatment(templates, result):
    '''Post-treatment of plots after template generate.

    For example add names from test result if not done before, suppress zero
    bins at range edges, etc.
    '''
    LOGGER.debug('calling post_treatment for %s', result.__class__)
    if 'Bonferroni' in result.__class__.__name__:
        LOGGER.debug('post already applied')
        return templates
    for templ in templates:
        for splt in templ.subplots:
            blimits = [trim_range(sc.bins) for sc in splt.curves]
            if all(not b[1] for a in blimits for b in a):
                continue
            nlimits = []
            for idim in range(len(blimits[0])):
                nlimits.append((min(crv[idim][0][0] for crv in blimits),
                                max(crv[idim][0][1] for crv in blimits)))
            splt.attributes.limits = nlimits
    return templates


def build_plot_template_with_dim(curves, axnames):
    '''Organise curves in :class:`~.templates.SubPlotElements`.

    If curves are 1D they will all go in the same
    :class:`~.templates.SubPlotElements`, if there are in 2 dimensions each
    curve will have its :class:`~.templates.SubPlotElements`.

    :param list(CurveElements) curves: list of curves
    :param list(str) axnames: list of axis names
    :rtype: list(SubPlotElements)
    '''
    dim = curves[0].values.ndim
    if dim == 1:
        subplot = SubPlotElements(curves=curves, axnames=axnames, ptype='1D')
        return PlotTemplate(subplots=[subplot], small_subplots=True,
                            suppress_xaxes=True, suppress_legends=True)
    if dim == 2:
        subplots = [SubPlotElements(curves=[crv], axnames=axnames, ptype='2D')
                    for crv in curves]
        return PlotTemplate(subplots=subplots, small_subplots=False)
    LOGGER.warning('Not expected dimension')
    return []


def repr_datasets_values(result):
    '''Representation of the datasets values from test results obtained from a
    child test of :class:`~valjean.gavroche.test.TestDataset`.

    Examples:

    * :class:`~valjean.gavroche.test.TestResultEqual`;
    * :class:`~valjean.gavroche.test.TestResultApproxEqual`;
    * :class:`~valjean.gavroche.stat_tests.student.TestResultStudent`.

    :param TestResult result: test result from test on datasets
    :rtype: list(PlotTemplate)

    If the dimension cannot be determined or if the dimension is greater than 2
    an empty list is returned.
    '''
    dab = dimensions_and_bins(result.test.dsref.bins,
                              result.test.dsref.value.shape)
    if dab is None:
        return []
    if len(dab) > 2:
        LOGGER.info('No plot available for %dD, no PlotTemplate built',
                    len(dab))
        return []
    cds = [CurveElements(
        values=result.test.dsref.value, bins=list(dab.values()),
        legend=(result.test.dsref.name if result.test.dsref.name
                else 'reference'),
        index=0, errors=result.test.dsref.error)]
    cds.extend([
        CurveElements(values=ds.value, bins=list(dab.values()),
                      legend=(ds.name if ds.name else 'dataset '+str(ids)),
                      index=ids+1, errors=ds.error)
        for ids, ds in enumerate(result.test.datasets)])
    pltemp = build_plot_template_with_dim(
        cds, axnames=list(dab.keys())+[result.test.dsref.what])
    return [pltemp] if pltemp else []


def repr_testresultequal(result, _verbosity=None):
    '''Represent the equal test result as a plot.

    :param TestResultEqual result: a test result.
    :rtype: list(PlotTemplate)
    '''
    return repr_datasets_values(result)


def repr_testresultapproxequal(result, _verbosity=None):
    '''Represent the approx equal test result as a plot.

    :param TestResultApproxEqual result: a test result.
    :rtype: list(PlotTemplate)
    '''
    return repr_datasets_values(result)


def repr_testresultstudent(result, verbosity=None):
    '''Plot the Student results according to verbosity.

    :param TestResultStudent result: a test result.
    :returns: Representation of a :class:`~.TestResultStudent` as a plot.
    :rtype: list(PlotTemplate)
    '''
    LOGGER.debug("PLOT student repr, %s, res = %s", verbosity, bool(result))
    # faire une condition sur le bool dans le cas de SUMMARY ?
    if verbosity in (Verbosity.SILENT, Verbosity.SUMMARY):
        return []
    if verbosity is None or verbosity == Verbosity.INTERMEDIATE:
        return repr_student_intermediate(result)
    if verbosity.value >= Verbosity.FULL_DETAILS.value:
        return repr_student_full_details(result)
    return repr_student_intermediate(result)


def repr_student_intermediate(result):
    '''Represent the Student test result as a plot.

    By default two :class:`~.templates.PlotTemplate` are returned in order to
    get a top plot representing the two series of values and the bottom plot
    representing the Δ from the Student test.

    :param TestResultStudent result:  a test result.
    :rtype: list(PlotTemplate)
    '''
    rval = repr_datasets_values(result)
    rdelta = repr_student_delta(result)
    rstudent = [join(rvals, rdelta)
                for rvals, rdelta in zip(rval, rdelta)]
    if not rstudent and rval:
        rstudent = rval
    return rstudent


def repr_student_full_details(result):
    '''Represent the Student test result as a plot.

    By default two :class:`~.templates.PlotTemplate` are returned in order to
    get a top plot representing the two series of values and the bottom plot
    representing the Δ from the Student test.

    :param TestResultStudent result:  a test result.
    :rtype: list(PlotTemplate)
    '''
    LOGGER.debug('in repr_student_full_details')
    rval = repr_datasets_values(result)
    rdelta = repr_student_delta(result)
    rpval = repr_student_pvalues(result)
    rstudent = [join(rvals, rdelta, rpvals)
                for rvals, rdelta, rpvals in zip(rval, rdelta, rpval)]
    if not rstudent and rval:
        rstudent = rval
    return rstudent


def repr_student_delta(result):
    '''Represent the Δ distribution from a Student test result as a plot.

    :param TestResultStudent result: a test result.
    :rtype: list(PlotTemplate)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.

    If the dimension cannot be determined an empty list is returned.
    '''
    dab = dimensions_and_bins(result.test.dsref.bins,
                              result.test.dsref.value.shape)
    if dab is None:
        return []
    if len(dab) > 2:
        LOGGER.info('No plot available for %dD, no PlotTemplate built',
                    len(dab))
        return []
    curves = [CurveElements(values=delta, legend='', bins=list(dab.values()),
                            index=ind+1, errors=None)
              for ind, delta in enumerate(result.delta)]
    pltemp = build_plot_template_with_dim(
        curves, axnames=list(dab.keys()) + [r'$t_{Student}$'])
    if not pltemp:
        return []
    if result.delta[0].ndim == 1:
        for splt in pltemp.subplots:
            splt.attributes.lines = [{'y': result.test.threshold},
                                     {'y': -result.test.threshold}]
    return [pltemp]


def repr_student_pvalues(result):
    '''Representation of p-values from Student test result as a plot.

    :param TestResultStudent result: a test result.
    :rtype: list(PlotTemplate)

    If p-values were not calculated, no :class:`~.PlotTemplate` is built, so
    an empty list is returned.
    '''
    if result.pvalue is None:
        LOGGER.debug("p-value is None, won't be possible to plot it.")
        return []
    dab = dimensions_and_bins(result.test.dsref.bins,
                              result.test.dsref.value.shape)
    if dab is None:
        return []
    if len(dab) > 2:
        LOGGER.info('No plot available for %dD, no PlotTemplate built',
                    len(dab))
        return []
    curves = [CurveElements(values=pval, bins=list(dab.values()),
                            legend='', index=ind+1, errors=None)
              for ind, pval in enumerate(result.pvalue)]
    pltemp = build_plot_template_with_dim(
        curves, axnames=list(dab.keys())+['p-value'])
    if not pltemp:
        return []
    if result.pvalue[0].ndim == 1:
        for splt in pltemp.subplots:
            splt.attributes.lines = [{'y': result.test.alpha/2},
                                     {'y': -result.test.alpha/2}]
    return [pltemp]


def repr_testresultmetadata(_result, _verbosity=None):
    '''Plot metadata test -> no plot done.

    :returns: empty list
    '''
    return []


def repr_testresultfailed(_result, _verbosity=None):
    '''Plot failed test -> no plot done.

    :returns: empty list
    '''
    return []


def repr_testresultstatstestsperflags(_result, _verbosity=None):
    '''Plot statistics on the tests classified per flags -> no plot done.

    :returns: empty list
    '''
    return []
