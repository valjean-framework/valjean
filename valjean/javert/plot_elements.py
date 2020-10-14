'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from collections import OrderedDict
import numpy as np
from .. import LOGGER
from ..cosette.task import TaskStatus
from ..gavroche.diagnostics.stats import TestOutcome
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
    subd = OrderedDict(items[i] for i in idims)
    return subd


def trim_range(bins, max_ratio=1000):
    '''Adapt bins range when extreme bins are very large.

    This function suggests reasonable ranges for the given bin axes by trimming
    the extreme bins if they are too wide. For each axis, the extreme bins are
    trimmed if their width is at least `max_ratio` times larger than the width
    of the neighbouring bin (the first bin is compared to the second one, and
    the last bin is compared to the second-last one). If there is no need to
    change the previous limits a tuple with initial limits is returned for the
    considered dimension. A boolean is associated to the tuple to precise if
    the limits have be changed.

    The trimmed ranges extend a bit over the clipped bins, so that their
    content is still visible in the plots.

    :param list(numpy.ndarray) bins: bins of the :class:`~.PlotTemplate`.
    :param float max_ratio: the bin size ratio above which bins will be
        truncated.
    :returns: new limits for all dimensions. The list has one item per
        dimension; the bool indicates whether the axis was actually trimmed.
    :rtype: list(tuple(float, float, bool))

    Examples:

    >>> bins = [np.array([-1e4, 0, 2, 4, 1e4]),
    ...         np.array([-1e2, 0, 2, 4, 1e4]),
    ...         np.array([-1e2, 0, 2, 4, 1e2])]
    >>> trim_range(bins)
    [(-0.2, 4.2, True), (-100.0, 9.2, True), (-100.0, 100.0, False)]
    '''
    LOGGER.debug('In plot_elements.trim_range')
    blimits = []
    for lbins in bins:
        nbins = lbins
        has_changed = [False, False]
        limits = [nbins[0], nbins[-1]]
        if lbins.dtype.kind == 'U':
            blimits.append([tuple(limits), False])
            continue
        if nbins.size < 3:
            LOGGER.warning('Not enough bins to adapt range.')
            blimits.append([tuple(limits), False])
            continue
        if nbins.size < 4:
            LOGGER.warning('Will adapt range for %d bins, '
                           'binning might be not suitable', nbins.size)
        binw = np.ediff1d(lbins)
        if binw[0]/binw[1] > max_ratio:
            limits[0] = nbins[1]
            has_changed[0] = True
        if binw[-1]/binw[-2] > max_ratio:
            limits[1] = nbins[-2]
            has_changed[1] = True
        rwidth = limits[1] - limits[0]
        if has_changed[0] or len(bins) == 1:
            limits[0] -= 0.05 * rwidth
        if has_changed[1] or len(bins) == 1:
            limits[1] += 0.05 * rwidth
        blimits.append((limits[0], limits[1], any(has_changed)))
    return blimits


def fit_curve_ranges(curves, threshold=0.0):
    '''Return a set of best-fit limits for the given curves.

    This function suggests axis limits for the given curves that make all
    curves fill the plot area. The limits are determined by looking at the
    region where any of the curves exceed the given threshold.

    :param list(CurveElements) curves: list of curves
    :param float threshold: threshold for the detection
    :returns: suggested limits for all dimensions
    :rtype: list((float, float))

    Example:

    >>> bins = [np.array([-1.0, 0.0, 1.0]),
    ...         np.array([0.0, 5.0, 10.0, 15.0])]
    >>> curve1 = CurveElements(np.array([[1.0, 2.0, 3.0],
    ...                                  [2.0, 3.0, 4.0]]),
    ...                       bins=bins, legend='curve1')
    >>> curve2 = CurveElements(np.array([[1.0, 4.0, 3.0],
    ...                                  [2.0, 3.0, 2.0]]),
    ...                       bins=bins, legend='curve2')
    >>> fit_curve_ranges([curve1, curve2], threshold = 3.5)
    [(-1.0, 1.0), (5.0, 15.0)]
    '''
    if not curves:
        return []
    c_limits = np.array([curve_limits(curve, threshold) for curve in curves])
    # the shape of c_limits here is (n_curves, n_axes, 2)
    unions = ranges_union(c_limits)
    # the shape of unions here is (n_axes, 2)
    return [(union[0], union[1]) for union in unions]


def ranges_union(ranges, union_axis=0, minmax_axis=-1):
    '''Return the union of the given ranges, axis by axis.

    :param ranges: an n-dimensional array of range bounds. The array shape can
        be anything, as long as one of the dimensions has length 2; this axis
        is assumed to contain the ``(min_range, max_range)`` pair.
    :type ranges: list or numpy.ndarray
    :param union_axis: the axis along which the union will be computed. If
        unspecified, the first axis will be assumed.
    :type union_axis: anything that `NumPy` understands as an axis.
    :param minmax_axis: the length-2 axis along which the range minimum and
        maximum are stored. If unspecified, the last axis will be assumed.
    :type minmax_axis: int
    :returns: an array of union bounds, with the same shape as the input array
        except for the suppression of `union_axis`.
    :rtype: numpy.ndarray

    Examples:

    >>> ranges_union([[(-1, 1)]])
    array([[-1,  1]])

    >>> ranges_union([[(-5, 5)], [(-3, 8)]])
    array([[-5,  8]])

    >>> ranges_union([[(-5, 5), (-1, 1)],
    ...               [(-3, 8), (-2, 2)]])
    array([[-5,  8],
           [-2,  2]])

    >>> ranges_union([[(-5, 5), (-1, 1)],
    ...               [(-3, 8), (-2, 2)],
    ...               [(-7, 1), (0, 6)]])
    array([[-7,  8],
           [-2,  6]])
    '''
    if not isinstance(ranges, np.ndarray):
        ranges = np.array(ranges)
    min_limits = np.min(ranges.take(0, minmax_axis), axis=union_axis)
    max_limits = np.max(ranges.take(1, minmax_axis), axis=union_axis)
    result = np.stack((min_limits, max_limits), axis=minmax_axis)
    return result


def curve_limits(curve, threshold=0.0):
    '''Return the set of bounds over each axis where the given curve exceeds
    the given threshold.

    For example, the following curve exceeds the threshold value of 50 in the
    central bins, which corresponds to `2.0<x<4.0` and `-0.5<y<0.5`:

    >>> bins = [np.linspace(0.0, 6.0, num=7),
    ...         np.linspace(-2.5, 2.5, num=6)]
    >>> curve = CurveElements(np.array([[  1,   1,   1,   1,   1],
    ...                                 [  1,  10,  30,  10,   1],
    ...                                 [  1,  10, 100,  10,   1],
    ...                                 [  1,  10, 100,  10,   1],
    ...                                 [  1,  10,  30,  10,   1],
    ...                                 [  1,   1,   1,   1,   1]]),
    ...                      bins=bins, legend='curve')
    >>> curve_limits(curve, threshold=50)
    [(2.0, 4.0), (-0.5, 0.5)]

    Changing the threshold to 20 modifies the range for the first axis, but
    not for the second one.

    >>> curve_limits(curve, threshold=20)
    [(1.0, 5.0), (-0.5, 0.5)]

    The function also works if the number of bin edges is equal to the number
    of values along a given direction (as opposed to the number of values plus
    one):

    >>> bins = [np.array([-1.0, 1.0]), np.array([0.0, 5.0, 10.0, 15.0])]
    >>> curve = CurveElements(np.array([[1.0, 2.0, 3.0],
    ...                                 [2.0, 3.0, 4.0]]),
    ...                      bins=bins, legend='curve')
    >>> curve_limits(curve, threshold = 3.5)
    [(1.0, 1.0), (10.0, 15.0)]
    '''
    limits = []
    n_dims = len(curve.bins)
    mask_nd = curve.values > threshold
    LOGGER.debug('mask_nd: %s', mask_nd)
    for i_bin, a_bin in enumerate(curve.bins):
        axis = tuple(i for i in range(n_dims) if i != i_bin)
        mask = mask_nd.any(axis=axis)
        LOGGER.debug('mask: %s', mask)
        if len(a_bin) == len(mask):
            over_thr_min = a_bin[mask]
            over_thr_max = a_bin[mask]
        else:  # here len(mask) + 1 == len(a_bin)
            over_thr_min = a_bin[:-1][mask]
            over_thr_max = a_bin[1:][mask]
        limits.append((np.amin(over_thr_min), np.amax(over_thr_max)))
    return limits


def pad_range(limits, log, padding=0.05):
    '''Pad the given limits.

    This function adds a bit of padding to the input limit range. If `log` is
    `False`, the new limits will be ``(limits[0] - padding * delta, limits[1] +
    padding * delta)``, where ``delta = limits[1] - limits[0]``. In log scale
    (`log=True`), the padded limits are ``(limits[0] * exp(-padding *
    log_delta), limits[1] * exp(padding * log_delta)``, with ``log_delta =
    log(limits[1] / limits[0])``.

    :param (float, float) limits: a pair of floats.
    :param bool log: whether we are in log scale.
    :param float padding: the amount of padding to insert.
    :returns: new limits
    :rtype: (float, float)
    '''
    if log:
        delta = np.exp(0.5 * padding * np.log(limits[1] / limits[0]))
        return limits[0] / delta, limits[1] * delta
    delta = 0.5 * padding * (limits[1] - limits[0])
    return limits[0] - delta, limits[1] + delta


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
            if splt.ptype not in ('1D', '2D'):
                continue
            blimits = [trim_range(sc.bins) for sc in splt.curves]
            if all(not b[1] for a in blimits for b in a):
                continue
            nlimits = []
            for idim in range(len(blimits[0])):
                nlimits.append((min(crv[idim][0] for crv in blimits),
                                max(crv[idim][1] for crv in blimits)))
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
    cds.extend(
        CurveElements(values=ds.value, bins=list(dab.values()),
                      legend=(ds.name if ds.name else 'dataset '+str(ids)),
                      index=ids+1, errors=ds.error)
        for ids, ds in enumerate(result.test.datasets))
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
        rstudent = [join(rvals, rdelta) for rvals, rdelta in zip(rval, rdelta)]
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


def repr_testresultexternal(_result, _verbosity=None):
    '''Plot external test -> no plot done.

    If plots are required they are already done. Their representation in the
    report is done by :class:`.ExternalRepresenter`.

    :returns: empty list
    '''
    return []


def repr_testresultfailed(_result, _verbosity=None):
    '''Plot failed test -> no plot done.

    :returns: empty list
    '''
    return []


def repr_testresultstats(result, status_ok, label):
    '''Represent result from statistical test as a plot (pie chart probably).

    Null results are omitted from the table.

    :param TestResult result: result from a statistical test
    :rtype: list(PlotTemplate)
    '''
    classify = result.classify
    statuses = [status_ok]
    statuses.extend(status for status in status_ok.__class__
                    if status != status_ok)
    counts = [len(classify[status]) for status in statuses]
    statuses = [status for status, count in zip(statuses, counts)
                if count != 0]
    counts = [count for count in counts if count != 0]
    statuses_txt = [status.name for status in statuses]
    subplot = SubPlotElements(
        curves=[CurveElements(values=np.array(counts),
                              bins=[np.array(statuses_txt)],
                              legend='')],
        axnames=(label, ''), ptype='pie')
    return [PlotTemplate(subplots=[subplot], small_subplots=False)]


def repr_testresultstatstasks(result, _verbosity=None):
    '''Represent result from statistical test on tasks as a plot (pie chart).

    :param TestResultStatsTasks result: result from tasks statistics
    :rtype: list(PlotTemplate)
    '''
    return repr_testresultstats(result, TaskStatus.DONE, 'Tasks')


def repr_testresultstatstests(result, _verbosity=None):
    '''Represent result from statistical test on tests as a plot (pie chart).

    :param TestResultStatsTests result: result from tasks statistics
    :rtype: list(PlotTemplate)
    '''
    return repr_testresultstats(result, TestOutcome.SUCCESS, 'Tests')


def repr_statstestsby2labels(result):
    '''Plot statistics on the tests classified by 2 labels.

    Caution: the tests are summed over the second label, only the first one
    will be written on the plot. This is for summaries.

    :rtype: list(PlotTemplate)
    '''
    keys = sorted(set(res['labels'][0] for res in result.classify))
    dok, dko = (OrderedDict([(k, 0) for k in keys]) for i in range(2))
    for res in result.classify:
        if res['KO'] == 0:
            dok[res['labels'][0]] += 1
        else:
            dko[res['labels'][0]] += 1
    labs = result.test.by_labels
    yname = '# of {} in {}'.format(labs[1], labs[0])
    curve_ok = CurveElements(np.array(list(dok.values())), bins=[keys],
                             index=0, legend='OK')
    curve_ko = CurveElements(np.array(list(dko.values())), bins=[keys],
                             index=1, legend='KO')
    sbpeb = SubPlotElements(curves=[curve_ok, curve_ko],
                            axnames=[labs[0], yname], ptype='bar')
    sbpebs = SubPlotElements(curves=[curve_ok, curve_ko],
                             axnames=[labs[0], yname], ptype='barstack')
    return [PlotTemplate(subplots=[sbpeb, sbpebs], small_subplots=False)]


def repr_testresultstatstestsbylabels(result, _verbosity=None):
    '''Plot statistics on the tests classified by labels if 1 or labels.

    :rtype: list(PlotTemplate)
    '''
    if len(result.test.by_labels) > 2:
        LOGGER.info('No plot for more than 2 labels.')
        return []
    if len(result.test.by_labels) == 2:
        return repr_statstestsby2labels(result)
    lok, lko, legs = ([] for i in range(3))
    for res in result.classify:
        lok.append(res['OK'])
        lko.append(res['KO'])
        legs.append(res['labels'][0])
    curve_ok = CurveElements(np.array(lok), bins=[legs], index=0, legend='OK')
    curve_ko = CurveElements(np.array(lko), bins=[legs], index=1, legend='KO')
    sbpeb = SubPlotElements(curves=[curve_ok, curve_ko],
                            axnames=[result.test.by_labels[0], '# of tests'],
                            ptype='bar')
    sbpebs = SubPlotElements(curves=[curve_ok, curve_ko],
                             axnames=[result.test.by_labels[0], '# of tests'],
                             ptype='barstack')
    return [PlotTemplate(subplots=[sbpeb, sbpebs], small_subplots=False)]
